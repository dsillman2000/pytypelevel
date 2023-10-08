from functools import reduce
from itertools import repeat
from typing import Annotated, Callable, Generic, Iterable, TypeVar

import attrs
from annotated_types import Ge

from pytypelevel.annotations import SupportsEq
from pytypelevel.kernel.semigroup import Semigroup

T = TypeVar('T', bound=SupportsEq)


class Monoid(Generic[T], Semigroup[T]):

    empty: T

    def __init__(self, __combine: Callable[[T, T], T], __empty: T):
        super().__init__(__combine)
        self.empty = __empty

    def is_empty(self, __a: T) -> bool:
        return __a == self.empty
    
    # override
    def combine_n(self, __a: T, __n: Annotated[int, Ge(0)]) -> T:
        return reduce(self._combine, repeat(__a, __n), self.empty)
    
    def combine_all(self, __a_values: Iterable[T]) -> T:
        return reduce(self._combine, __a_values, self.empty)
    
    def reverse(self) -> "Monoid[T]":
        __combine = self._combine
        return Monoid[T](lambda a, b: __combine(b, a), self.empty)