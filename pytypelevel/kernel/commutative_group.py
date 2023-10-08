from typing import Generic, TypeVar

from pytypelevel.kernel.commutative_monoid import CommutativeMonoid
from pytypelevel.kernel.group import Group

T = TypeVar('T')

class CommutativeGroup(Generic[T], Group[T], CommutativeMonoid[T]):
    pass