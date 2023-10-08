from typing import Generic, TypeVar

from pytypelevel.kernel.band import Band
from pytypelevel.kernel.commutative_semigroup import CommutativeSemigroup
from pytypelevel.kernel.eq import Eq
from pytypelevel.kernel.partial_order import PartialOrder

T = TypeVar('T')

class Semilattice(Generic[T], Band[T], CommutativeSemigroup[T]):

    def as_meet_partial_order(self, __eq: Eq[T]) -> PartialOrder[T]:

        def _meet_pcmp(__x: T, __y: T) -> float:
            if __eq.eqv(__x, __y):
                return 0.0
            __z = self.combine(__x, __y)
            if __eq.eqv(__x, __z): return -1.0
            elif __eq.eqv(__y, __z): return 1.0
            return float('nan')
        
        return PartialOrder[T](_meet_pcmp)
    
    def as_join_partial_order(self, __eq: Eq[T]) -> PartialOrder[T]:

        def _join_pcmp(__x: T, __y: T) -> float:
            if __eq.eqv(__x, __y):
                return 0.0
            __z = self.combine(__x, __y)
            if __eq.eqv(__y, __z): return -1.0
            elif __eq.eqv(__x, __z): return 1.0
            return float('nan')
        
        return PartialOrder[T](_join_pcmp)