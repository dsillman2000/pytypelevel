from typing import Annotated, Generic, TypeVar

from annotated_types import Ge

from pytypelevel.kernel.commutative_monoid import CommutativeMonoid
from pytypelevel.kernel.semilattice import Semilattice

T = TypeVar('T')


class BoundedSemilattice(Generic[T], CommutativeMonoid[T], Semilattice[T]):

    def combine_n(self, __t: T, __n: Annotated[int, Ge(0)]) -> T:
        if __n == 0: self.empty
        return __t  # in semilattices, combine(t, t) = t