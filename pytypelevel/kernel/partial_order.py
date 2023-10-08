import operator
from typing import Callable, Generic, Optional, TypeVar, overload

import attrs

from pytypelevel.kernel.eq import Eq

T = TypeVar('T')
U = TypeVar('U')

"""
Cats partial comparison truth table:

 * | x <= y | x >= y | result | note |
 * | :--    | :--    | --:    | :-- |
 * | true   |true    | 0.0    | (corresponds to x = y) |
 * | false  |false   | NaN    | (x and y cannot be compared) |
 * | true   |false   | -1.0   | (corresponds to x < y) |
 * | false  |true    | 1.0    | (corresponds to x > y) |

"""

def _partial_cmp_from_le(__le: Callable[[T, T], bool]) -> Callable[[T, T], float]:
    def _pcmp(__a: T, __b: T):
        match __le(__a, __b), __le(__b, __a):
            case True, True:
                return 0.0
            case False, False:
                return float('nan')
            case True, False:
                return -1.0
            case _:
                return 1.0
    return _pcmp

class PartialOrder(Generic[T], Eq[T]):

    _partial_cmp: Callable[[T, T], float]

    def __init__(self, __partial_cmp: Callable[[T, T], float] = _partial_cmp_from_le(operator.le)): #type: ignore
        super().__init__((lambda a, b: __partial_cmp(a, b) == 0.0))
        self._partial_cmp = __partial_cmp
        
    def partial_compare(self, __x: T, __y: T) -> float:
        return self._partial_cmp(__x, __y)
    
    def try_compare(self, __x: T, __y: T) -> Optional[int]:
        try:
            return int(self.partial_compare(__x, __y))
        except ValueError:
            return None
        
    def pmin(self, __a: T, __b: T) -> Optional[T]:
        return None if not (_cmp := self.try_compare(__a, __b)) \
            else (None, __b, __a)[_cmp]
    
    def pmax(self, __a: T, __b: T) -> Optional[T]:
        return None if not (_cmp := self.try_compare(__a, __b)) \
            else (None, __a, __b)[_cmp]
    
    def eqv(self, __a: T, __b: T) -> bool:
        return self._partial_cmp(__a, __b) == 0
    
    def lteqv(self, __a: T, __b: T) -> bool:
        return self._partial_cmp(__a, __b) <= 0
    
    def lt(self, __a: T, __b: T) -> bool:
        return self._partial_cmp(__a, __b) < 0
    
    def gteqv(self, __a: T, __b: T) -> bool:
        return self._partial_cmp(__a, __b) >= 0
    
    def gt(self, __a: T, __b: T) -> bool:
        return self._partial_cmp(__a, __b) > 0
    
    def by(self, __f: Callable[[U], T]) -> "PartialOrder[U]":
        __partial_cmp = self._partial_cmp
        return PartialOrder[U](lambda x, y: __partial_cmp(__f(x), __f(y)))
    
    def reverse(self) -> "PartialOrder[T]":
        __partial_cmp = self._partial_cmp
        return PartialOrder[T](lambda a, b: __partial_cmp(b, a))