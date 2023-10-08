from typing import Generic, Self, TypeVar

from pytypelevel.kernel.commutative_semigroup import CommutativeSemigroup
from pytypelevel.kernel.monoid import Monoid

T = TypeVar('T')

class CommutativeMonoid(Generic[T], Monoid[T], CommutativeSemigroup[T]):

    def reverse(self) -> "CommutativeMonoid[T]": return self