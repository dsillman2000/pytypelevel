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

    def combine_n(self, a: T, n: Annotated[int, Gt(0)]) -> T:
        return reduce(self._combine, repeat(a, (n - 1)), a)
    
    def combine_all_option(self, a_values: Iterable[T]) -> Optional[T]:
        try:
            return reduce(self._combine, a_values)
        except TypeError:
            return None
        
    def reverse(self) -> "Semigroup[T]":
        __combine = self._combine
        return Semigroup[T](lambda a, b: __combine(b, a))

    def intercalate(self, middle: T) -> "Semigroup[T]":
        __combine = self._combine
        return Semigroup[T](lambda a, b: __combine(a, __combine(middle, b)))

    @overload
    def maybe_combine(self, oa: Optional[T], ob: T) -> T: ...
    @overload
    def maybe_combine(self, oa: T, ob: Optional[T]) -> T: ...

    def maybe_combine(self, oa, ob) -> T:
        match oa, ob:
            case None, None: raise TypeError()
            case None, _: return ob
            case _, None: return oa
            case _: return self.combine(oa, ob)