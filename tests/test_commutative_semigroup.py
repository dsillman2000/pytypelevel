import operator

from pytypelevel import CommutativeSemigroup


def test_commutative_semigroup_instances__intmul():

    intmul = CommutativeSemigroup[int](operator.mul)

    assert intmul.combine(3, 7) == intmul.combine(7, 3) == 21
    assert intmul.reverse() == intmul
    assert intmul.intercalate(2).combine(3, 4) == 24

def test_commutative_semigroup_instances__tupconcat():

    tupconcat = CommutativeSemigroup[tuple[int, ...]](operator.add)

    assert tupconcat.combine((1, 2, 3), (7, 8)) == (1, 2, 3, 7, 8)
    assert tupconcat.intercalate((1,)).combine((2, 3), (5, 6)) == (2, 3, 1, 5, 6)
    assert tupconcat.intercalate((1,)).combine_n((4,), 3) == (4, 4, 4, 1, 1)