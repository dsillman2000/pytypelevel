import operator
from typing import Callable, Generic, TypeVar, cast

from pytypelevel.kernel.monoid import Monoid
from pytypelevel.kernel.partial_order import PartialOrder

"""
Cats comparison truth table:

 * x <= y    x >= y      Int
 * true      true        = 0     (corresponds to x == y)
 * true      false       < 0     (corresponds to x < y)
 * false     true        > 0     (corresponds to x > y)
"""


T = TypeVar('T')
U = TypeVar('U')

def _cmp_from_lt(__lt: Callable[[T, T], bool]) -> Callable[[T, T], int]:
    def _cmp(__a: T, __b: T) -> int:
        match __lt(__a, __b), __lt(__b, __a):
            case True, False: return -1
            case False, True: return 1
            case _: return 0
    return _cmp

class Order(Generic[T], PartialOrder[T]):

    _cmp: Callable[[T, T], int]

    def __init__(self, __cmp: Callable[[T, T], int] = _cmp_from_lt(operator.lt)): # type: ignore
        super().__init__(__cmp)
        self._cmp = __cmp

    @staticmethod
    def from_lt(__lt: Callable[[T, T], bool] = operator.lt) -> "Order[T]": # type: ignore
        return Order[T](_cmp_from_lt(__lt))
    
    @staticmethod
    def from_le(__le: Callable[[T, T], bool] = operator.le) -> "Order[T]": # type: ignore
        return Order[T](_cmp_from_lt(__le))

    def compare(self, __a: T, __b: T) -> int:
        return self._cmp(__a, __b)
    
    def partial_compare(self, __a: T, __b: T) -> float:
        return float(self.compare(__a, __b))
    
    def min(self, __x: T, __y: T) -> T:
        return (__y, __x, __y)[self.compare(__y, __x)]
    
    def max(self, __x: T, __y: T) -> T:
        return (__y, __x, __y)[self.compare(__x, __y)]
    
    def eqv(self, __x: T, __y: T) -> bool:
        return self.compare(__x, __y) == 0
    
    def neqv(self, __x: T, __y: T) -> bool:
        return not self.eqv(__x, __y)
    
    def lteqv(self, __x: T, __y: T) -> bool:
        return self.compare(__x, __y) <= 0
    
    def lt(self, __x: T, __y: T) -> bool:
        return self.compare(__x, __y) < 0
    
    def gteqv(self, __x: T, __y: T) -> bool:
        return self.compare(__x, __y) >= 0
    
    def gt(self, __x: T, __y: T) -> bool:
        return self.compare(__x, __y) > 0
    
    def by(self, __f: Callable[[U], T]) -> "Order[U]":
        __cmp = self._cmp
        return Order[U](lambda a, b: __cmp(__f(a), __f(b)))
    
    def reverse(self) -> "Order[T]":
        __cmp = self._cmp
        return Order[T](lambda a, b: __cmp(b, a))
    
    @staticmethod
    def when_equal(__first: "Order[T]", __second: "Order[T]") -> "Order[T]":
        return Order[T](
            lambda a, b: __second._cmp(a, b) 
                if (fr := __first._cmp(a, b)) == 0 
                else fr
        )
    
    @staticmethod
    def all_equal() -> "Order[T]":
        return Order[T](lambda *_: 0)
    
    @staticmethod
    def when_equal_monoid() -> "Monoid[Order[T]]":
        return Monoid[Order[T]](Order[T].when_equal, Order[T].all_equal())