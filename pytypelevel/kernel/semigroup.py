import abc
from functools import reduce
from itertools import repeat
from typing import Annotated, Callable, Generic, Iterable, Optional, Type, TypeVar

from annotated_types import Gt

T = TypeVar('T')

class Semigroup(Generic[T]):
    
    _combine: Callable[[T, T], T]

    def __init__(self, combine: Callable[[T, T], T]):
        self._combine = combine

    def combine(self, t1: T, t2: T) -> T:
        return self._combine(t1, t2)

    def combine_n(self, a: T, n: Annotated[int, Gt(0)]) -> T:
        return reduce(self._combine, repeat(a, (n - 1)), a)
    
    def combine_all_option(self, a_values: Iterable[T]) -> Optional[T]:
        try:
            return reduce(self._combine, a_values)
        except TypeError:
            return None
        
    def reverse(self) -> "Semigroup[T]":
        __combine = self._combine
        return Semigroup[T](combine = lambda a, b: __combine(b, a))

    def intercalate(self, middle: T) -> "Semigroup[T]":
        __combine = self._combine
        return Semigroup[T](combine = lambda a, b: __combine(a, __combine(middle, b)))
