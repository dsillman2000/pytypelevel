from typing import Callable, Generic, TypeVar

from pytypelevel.kernel.monoid import Monoid

T = TypeVar('T')


class Group(Generic[T], Monoid[T]):

    _inv: Callable[[T], T]

    def __init__(self, __combine: Callable[[T, T], T], __empty: T, __inv: Callable[[T], T]):
        super().__init__(__combine, __empty)
        self._inv = __inv

    def inverse(self, __t: T) -> T:
        return self._inv(__t)

    def remove(self, __a: T, __b: T) -> T:
        return self.combine(__a, self.inverse(__b))
    
    def combine_n(self, __t: T, __n: int) -> T:
        if __n > 0:
            return super().combine_n(__t, __n)
        if __n < 0:
            return super().combine_n(self.inverse(__t), abs(__n))
        return self.empty