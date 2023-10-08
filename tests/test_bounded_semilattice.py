from typing import Annotated

from annotated_types import Gt

from pytypelevel import BoundedSemilattice, Eq


def test_bounded_semilattice_instances__minposint():

    posint = Annotated[int, Gt(0)]
    minposint = BoundedSemilattice[posint](min, 1)

    assert minposint.combine(3, 4) == 3 and minposint.combine(7, 1) == 1 and \
           minposint.combine_all([7, 2, 3, 5, 1]) == minposint.empty
    
    minposintmpo = minposint.as_meet_partial_order(Eq[int]())

    assert minposintmpo.partial_compare(1, 2) == -1.0 and minposintmpo.partial_compare(2, 1) == 1.0