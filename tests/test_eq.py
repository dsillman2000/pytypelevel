import operator

from pytypelevel import Eq


def test_eq_instances__streq():

    streq = Eq[str]()

    assert streq.eqv('a', 'a')
    assert streq.neqv('u', 'v')

    same_first_letter = Eq[str]().by(operator.itemgetter(0))
    same_last_letter = Eq[str]().by(operator.itemgetter(-1))

    assert same_first_letter.eqv('absolute', 'another')
    assert same_last_letter.neqv('absolute', 'another')
    assert same_first_letter.and_(same_last_letter).eqv('acura', 'anova')
    assert same_first_letter.and_(same_last_letter).neqv('aaa', 'aab')
    assert same_first_letter.or_(same_last_letter).eqv('aaa', 'aab')
    assert same_first_letter.or_(same_last_letter).neqv('john', 'alex')

    assert Eq[str].all_equal().eqv('anything', 'literally anything else')

def test_eq_instances__inteq():

    inteq = Eq[int]()

    assert inteq.eqv(172, 172)
    assert inteq.neqv(-20, 20)

    same_square: Eq[int] = Eq[int]().by(lambda u: u * u)
    same_sign: Eq[int] = Eq[int]().by(lambda u: u // max(1, abs(u)))

    assert same_square.eqv(-11, 11)
    assert same_sign.neqv(-10, 10)
    assert same_square.and_(same_sign).eqv(-8, -8)
    assert same_square.and_(same_sign).neqv(7, 8)
    assert same_square.or_(same_sign).eqv(7, 8)
    assert same_square.or_(same_sign).neqv(-7, 8)

    assert Eq[int].all_equal().eqv(-1, 0)

def test_eq_instances__tuples():

    permutation: Eq[tuple[int, ...]] = Eq(lambda t1, t2: sorted(t1) == sorted(t2))

    assert permutation.eqv((2, 7, 3), (3, 7, 2))
    assert permutation.neqv((2, 7, 3), (2, 7, 3, 3))

    alphabet: Eq[tuple[int, ...]] = Eq(lambda t1, t2: set(t1) == set(t2))

    assert alphabet.eqv((3, 7, 3, 3), (3, 7, 7))
    assert alphabet.neqv((3, 7, 3), (1, 1, 1))
    assert alphabet.and_(permutation).eqv((7, 7, 2), (2, 7, 7))
    assert alphabet.or_(permutation).neqv((1, 2, 3), (4, 5, 6))
    