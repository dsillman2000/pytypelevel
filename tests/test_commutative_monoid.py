from pytypelevel import CommutativeMonoid

from .conftest import Pair


def test_commutative_monoid_instances__pairsum():

    pairsum = CommutativeMonoid[Pair](lambda a, b: (a[0] + b[0], a[1] + b[1]), (0, 0))

    assert pairsum.combine((2, 3), (1, 0)) == (3, 3)
    assert pairsum.combine_all([(2, 0), (1, 1), (0, 2)]) == (3, 3)
    assert pairsum.reverse().combine_all([(2, 0), (1, 1), (0, 2)]) == (3, 3)