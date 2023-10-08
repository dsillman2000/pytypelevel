import operator

from pytypelevel import Band


def test_band_instances__dictmerge():

    dictmerge = Band[dict](operator.ior)

    assert dictmerge.combine({'a': 1}, {'b': 2}) == {'a': 1, 'b': 2}
    assert dictmerge.combine({'a': 0}, {'a': 0}) == {'a': 0}

    assert dictmerge.combine_n({'x': 3}, int(1e27)) == {'x': 3}


def test_band_instances__idempotent_add():

    idempotent_add = Band[int](operator.add)

    assert idempotent_add.combine(7, 2) == 9
    assert idempotent_add.combine(7, 7) == 7
    assert idempotent_add.combine_all_option([1, 2, 3]) == 3