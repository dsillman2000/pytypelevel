from pytypelevel import Eq, Semilattice


def test_semilattice_instances__max():

    maximum = Semilattice[float](max)

    assert maximum.combine(2.0, 3.0) == 3.0 and \
           maximum.combine(4.0, -1.0) == maximum.combine(-1.0, 4.0) ==  4.0 and \
           maximum.combine(0.0, 0.0) == 0.0
    assert maximum.combine_all_option([1.0, -7.0, 2.0, -8.0]) == 2.0
    
    maxjpo = maximum.as_join_partial_order(Eq[float]())
    
    assert maxjpo.partial_compare(-7.0, -14.0) == 1.0 \
           and maxjpo.pmin(8.0, 80.0) == 8.0 \
           and maxjpo.pmax(17.0, 3.0) == 17.0
    

def test_semilattice_instances__min():

    minimum = Semilattice[float](min)

    assert minimum.combine(2.0, 3.0) == 2.0 and \
           minimum.combine(4.0, -1.0) == -1.0 and minimum.combine(-1.0, 4.0) == -1.0 and \
           minimum.combine(0.0, 0.0) == 0.0
    assert minimum.combine_all_option([1.0, -7.0, 2.0, -8.0]) == -8.0

    minmpo = minimum.as_meet_partial_order(Eq[float]())

    assert minmpo.partial_compare(-7.0, -14.0) == 1.0 \
           and minmpo.pmin(8.0, 80.0) == 8.0 \
           and minmpo.pmax(17.0, 3.0) == 17.0