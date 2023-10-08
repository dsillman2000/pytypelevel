from functools import reduce
from itertools import repeat
from typing import Annotated, Callable, Generic, Iterable, Optional, TypeVar, overload

from annotated_types import Gt

T = TypeVar('T')

class Semigroup(Generic[T]):
    
    _combine: Callable[[T, T], T]

    def __init__(self, __combine: Callable[[T, T], T]):
        self._combine = __combine

    def combine(self, __t1: T, __t2: T) -> T:
        return self._combine(__t1, __t2)

    def combine_n(self, __a: T, __n: Annotated[int, Gt(0)]) -> T:
        return reduce(self._combine, repeat(__a, (__n - 1)), __a)
    
    def combine_all_option(self, __a_values: Iterable[T]) -> Optional[T]:
        try:
            return reduce(self._combine, __a_values)
        except TypeError:
            return None
        
    def reverse(self) -> "Semigroup[T]":
        __combine = self._combine
        return Semigroup[T](lambda a, b: __combine(b, a))

    def intercalate(self, __middle: T) -> "Semigroup[T]":
        __combine = self._combine
        return Semigroup[T](lambda a, b: __combine(a, __combine(__middle, b)))

    @overload
    def maybe_combine(self, __oa: Optional[T], __ob: T) -> T: ...
    @overload
    def maybe_combine(self, __oa: T, __ob: Optional[T]) -> T: ...

    def maybe_combine(self, __oa, __ob) -> T:
        match __oa, __ob:
            case None, None: raise TypeError()
            case None, _: return __ob
            case _, None: return __oa
            case _: return self.combine(__oa, __ob)

    @staticmethod
    def first() -> "Semigroup[T]":
        return Semigroup[T](lambda a, _: a)
    
    @staticmethod
    def last() -> "Semigroup[T]":
        return Semigroup[T](lambda _, b: b)