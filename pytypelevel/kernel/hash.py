from typing import Callable, Generic, TypeVar

from pytypelevel.kernel.eq import Eq

T = TypeVar('T')
U = TypeVar('U')

class Hash(Generic[T], Eq[T]):

    _hash: Callable[[T], int]

    def __init__(self, __hash: Callable[[T], int] = hash):
        super().__init__(Eq[int]().by(__hash)._eqv)
        self._hash = __hash

    def by(self, __f: Callable[[U], T]) -> "Hash[U]":
        __hash = self._hash
        return Hash[U](lambda u: __hash(__f(u)))