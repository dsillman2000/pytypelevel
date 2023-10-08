from pytypelevel import Hash


def test_hash_instances__str():
    
    h = Hash[str]()

    assert h.eqv('complex string', 'complex string')
    assert h.neqv('cimplex string', 'complex string')
    
    permutation: Hash[str] = Hash[str]().by(lambda s: ''.join(sorted(s)))

    assert permutation.neqv('ample', 'good')
    assert permutation.eqv('sample', 'maples')
