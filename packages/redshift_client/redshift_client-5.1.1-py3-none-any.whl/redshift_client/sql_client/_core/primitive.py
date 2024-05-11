from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    FrozenDict,
)
from fa_purity._core.coproduct import (
    Coproduct,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.json_2.primitive import (
    JsonPrimitive,
    JsonPrimitiveFactory,
    Primitive,
)
from fa_purity.pure_iter import (
    PureIterFactory,
)
from fa_purity.result import (
    ResultE,
    ResultFactory,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_purity.union import (
    CoproductFactory,
)
from fa_purity.utils import (
    cast_exception,
)
from typing import (
    Callable,
    TypeVar,
)

DbPrimitive = Coproduct[JsonPrimitive, datetime]
_A = TypeVar("_A")
_T = TypeVar("_T")
_R = TypeVar("_R")


@dataclass(frozen=True)
class DbPrimitiveFactory:
    @staticmethod
    def from_raw(raw: Primitive | datetime) -> DbPrimitive:
        if isinstance(raw, datetime):
            return Coproduct.inr(raw)
        return Coproduct.inl(JsonPrimitiveFactory.from_raw(raw))

    @classmethod
    def from_raw_dict(
        cls, raw: FrozenDict[str, Primitive | datetime]
    ) -> FrozenDict[str, DbPrimitive]:
        return FrozenDict({k: cls.from_raw(v) for k, v in raw.items()})

    @classmethod
    def from_raw_prim_dict(
        cls, raw: FrozenDict[str, Primitive]
    ) -> FrozenDict[str, DbPrimitive]:
        return FrozenDict({k: cls.from_raw(v) for k, v in raw.items()})

    @staticmethod
    def from_any(raw: _T) -> ResultE[DbPrimitive]:
        factory: ResultFactory[DbPrimitive, Exception] = ResultFactory()
        factory2: CoproductFactory[
            JsonPrimitive, datetime
        ] = CoproductFactory()
        return (
            JsonPrimitiveFactory.from_any(raw)
            .map(lambda p: factory2.inl(p))
            .lash(
                lambda _: factory.success(factory2.inr(raw))
                if isinstance(raw, datetime)
                else factory.failure(
                    ValueError(
                        f"not a `datetime` nor `JsonPrimitive`; got {type(raw)}"
                    )
                ).alt(cast_exception)
            )
        )

    @staticmethod
    def to_list_of(
        items: _A, assertion: Callable[[_T], ResultE[_R]]
    ) -> ResultE[FrozenList[_R]]:
        factory: ResultFactory[FrozenList[_R], Exception] = ResultFactory()
        if isinstance(items, tuple):
            return all_ok(
                PureIterFactory.from_list(items).map(assertion).to_list()  # type: ignore[misc]
            )
        return factory.failure(TypeError("Expected tuple")).alt(Exception)
