import operator
from typing import Callable, Generic, TypeVar

from pytypelevel.annotations import SupportsEq

T = TypeVar('T')
U = TypeVar('U')


class Eq(Generic[T]):

    _eqv: Callable[[T, T], bool]

    def __init__(self, __oeq: Callable[[T, T], bool] = operator.eq):
        self._eqv = __oeq

    def eqv(self, __t1: T, __t2: T) -> bool:
        return self._eqv(__t1, __t2)
    
    def neqv(self, __t1: T, __t2: T) -> bool:
        return not self._eqv(__t1, __t2)

    def by(self, __f: Callable[[U], T]) -> "Eq[U]": 
        __eqv = self._eqv
        return Eq[U](lambda a, b: __eqv(__f(a), __f(b)))
    
    def and_(self, __eq: "Eq[T]") -> "Eq[T]":
        return Eq[T](lambda a, b: self.eqv(a, b) and __eq.eqv(a, b))
    
    def or_(self, __eq: "Eq[T]") -> "Eq[T]":
        return Eq[T](lambda a, b: self.eqv(a, b) or __eq.eqv(a, b))
    
    @classmethod
    def all_equal(cls) -> "Eq[T]":
        return Eq[T](lambda *_: True)
        