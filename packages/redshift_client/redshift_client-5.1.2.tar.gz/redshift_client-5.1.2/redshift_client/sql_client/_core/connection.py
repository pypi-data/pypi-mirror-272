from __future__ import (
    annotations,
)

from .creds import (
    Credentials,
    DatabaseId,
)
from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity.cmd import (
    Cmd,
    CmdUnwrapper,
)
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions
from typing import (
    Any,
    Callable,
    NoReturn,
    TYPE_CHECKING,
    TypeVar,
)

if TYPE_CHECKING:
    from psycopg2 import (
        connection as ConnectionStub,
        cursor as CursorStub,
    )
else:
    CursorStub = Any
    ConnectionStub = Any


_T = TypeVar("_T")


class IsolationLvl(Enum):
    READ_UNCOMMITTED = postgres_extensions.ISOLATION_LEVEL_READ_UNCOMMITTED
    READ_COMMITTED = postgres_extensions.ISOLATION_LEVEL_READ_COMMITTED
    REPEATABLE_READ = postgres_extensions.ISOLATION_LEVEL_REPEATABLE_READ
    SERIALIZABLE = postgres_extensions.ISOLATION_LEVEL_SERIALIZABLE


@dataclass(frozen=True)
class _DbConnection:
    _connection: ConnectionStub

    def act(self, action: Callable[[ConnectionStub], _T]) -> Cmd[_T]:
        return Cmd.from_cmd(lambda: action(self._connection))

    @staticmethod
    def connect(
        db_id: DatabaseId,
        creds: Credentials,
        readonly: bool,
        isolation: IsolationLvl,
        autocommit: bool,
    ) -> Cmd[_DbConnection]:
        def _action() -> _DbConnection:
            connection = postgres.connect(
                dbname=db_id.db_name,
                user=creds.user,
                password=creds.password,
                host=db_id.host,
                port=db_id.port,
            )
            connection.set_session(
                isolation_level=isolation.value,
                readonly=readonly,
                autocommit=autocommit,
            )
            return _DbConnection(connection)

        return Cmd.from_cmd(_action)


@dataclass(frozen=True)
class DbConnection:
    _inner: _DbConnection

    def close(self) -> Cmd[None]:
        return self._inner.act(lambda c: c.close())

    def commit(self) -> Cmd[None]:
        return self._inner.act(lambda c: c.commit())

    def act_on_cursor(self, action: Callable[[CursorStub], _T]) -> Cmd[_T]:
        return self._inner.act(lambda c: action(c.cursor()))

    @staticmethod
    def connect_and_execute(
        db_id: DatabaseId,
        creds: Credentials,
        readonly: bool,
        isolation: IsolationLvl,
        autocommit: bool,
        action: Callable[[DbConnection], Cmd[_T | NoReturn]],
    ) -> Cmd[_T]:
        """Ensures that connection is closed regardless of action errors"""

        def _inner(connection: DbConnection) -> Cmd[_T]:
            def _action(unwrapper: CmdUnwrapper) -> _T:
                try:
                    return unwrapper.act(action(connection))
                finally:
                    unwrapper.act(connection.close())

            return Cmd.new_cmd(_action)

        return (
            _DbConnection.connect(
                db_id,
                creds,
                readonly,
                isolation,
                autocommit,
            )
            .map(DbConnection)
            .bind(_inner)
        )
