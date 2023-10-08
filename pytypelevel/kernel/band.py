from typing import Annotated, Callable, Generic, TypeVar

from annotated_types import Gt

from pytypelevel.annotations import SupportsEq
from pytypelevel.kernel.semigroup import Semigroup

T = TypeVar('T', bound=SupportsEq)

class Band(Generic[T], Semigroup[T]):

    def __init__(self, __combine: Callable[[T, T], T]):
        def _idempotent_combine(__t1: T, __t2: T) -> T:
            return __combine(__t1, __t2) if __t1 != __t2 else __t1
        super().__init__(_idempotent_combine)

    def combine_n(self, __a: T, __n: Annotated[int, Gt(0)]) -> T:
        return __a