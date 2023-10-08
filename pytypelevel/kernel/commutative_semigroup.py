import types
from typing import Annotated, Generic, TypeVar

from annotated_types import Gt

from pytypelevel.kernel.semigroup import Semigroup

T = TypeVar('T')


class CommutativeSemigroup(Generic[T], Semigroup[T]):

    def reverse(self) -> "CommutativeSemigroup[T]":
        return self
    
    def intercalate(self, __middle: T) -> "CommutativeSemigroup[T]":
        # a + m + a ... = combine_n(a, n) + combine_n(middle, n - 1)
        _intercalated = super().intercalate(__middle)
        _commut = CommutativeSemigroup[T](_intercalated._combine)
        def _interc_comb_n(__a: T, __n: Annotated[int, Gt(0)]) -> T:
            return self.combine(self.combine_n(__a, __n), self.combine_n(__middle, __n - 1))
        _commut.combine_n = types.MethodType(_interc_comb_n, _commut)
        return _commut