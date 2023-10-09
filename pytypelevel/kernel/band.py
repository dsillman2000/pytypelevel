from typing import Annotated, Callable, Generic, TypeVar

from annotated_types import Gt

from pytypelevel.annotations import SupportsEq
from pytypelevel.kernel.semigroup import Semigroup

T = TypeVar('T', bound=SupportsEq)



class Band(Generic[T], Semigroup[T]):

    def __init__(self, __idempotent_combine: Callable[[T, T], T]):
        super().__init__(__idempotent_combine)

    def combine_n(self, __a: T, __n: Annotated[int, Gt(0)]) -> T:
        return __a