from fa_purity import (
    FrozenDict,
)
from fa_purity.json_2.primitive import (
    JsonPrimitive,
)
from fa_purity.union import (
    Coproduct,
)
from redshift_client.core.column import (
    Column,
)
from redshift_client.core.data_type.core import (
    DataType,
    StaticTypes,
)
from redshift_client.core.id_objs import (
    ColumnId,
    Identifier,
)
from redshift_client.core.table import (
    Table,
)
from redshift_client.sql_client._core.primitive import (
    DbPrimitiveFactory,
)

_column_1 = ColumnId(Identifier.new("column_1"))
_column_2 = ColumnId(Identifier.new("column_2"))
_mock_type = Column(
    DataType(StaticTypes.BOOLEAN), False, DbPrimitiveFactory.from_raw(None)
)


def test_missing_order() -> None:
    assert Table.new(
        (_column_2,), FrozenDict({_column_1: _mock_type}), frozenset([])
    ).unwrap_fail()


def test_duplicated_order() -> None:
    assert Table.new(
        (_column_2, _column_2, _column_1),
        FrozenDict({_column_1: _mock_type, _column_2: _mock_type}),
        frozenset([]),
    ).unwrap_fail()


def test_missing_columns() -> None:
    assert Table.new(
        (_column_2, _column_1),
        FrozenDict({_column_2: _mock_type}),
        frozenset([]),
    ).unwrap_fail()


def test_invalid_key() -> None:
    assert Table.new(
        (_column_1,),
        FrozenDict({_column_1: _mock_type}),
        frozenset([_column_2]),
    ).unwrap_fail()


def test_valid() -> None:
    assert Table.new(
        (_column_2, _column_1),
        FrozenDict({_column_1: _mock_type, _column_2: _mock_type}),
        frozenset([_column_2]),
    ).unwrap()
