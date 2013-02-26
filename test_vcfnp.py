"""
Some simple unit tests for the vcfnp extension.

"""


from vcfnp import variants, info, calldata
from nose.tools import eq_


def test_variants():
    a = variants('sample.vcf', arities={'ALT': 2})
    print repr(a)
    eq_(9, len(a))
    eq_('19', a[0]['CHROM'])
    eq_(111, a[0]['POS'])
    eq_('rs6054257', a[2]['ID'])
    eq_('A', a[0]['REF'])
    eq_('ATG', a[8]['ALT'][1])
    eq_(10.0, a[1]['QUAL'])
    eq_(True, a[2]['FILTER']['PASS'])
    eq_(False, a[3]['FILTER']['PASS'])
    eq_(True, a[3]['FILTER']['q10'])
    eq_(2, a[0]['num_alleles'])
    eq_(False, a[5]['is_snp'])
    
#array([ ('19', 111, '.', 'A', ['C', ''], 9.600000381469727, (False, False, False), 2, True),
#       ('19', 112, '.', 'A', ['G', ''], 10.0, (False, False, False), 2, True),
#       ('20', 14370, 'rs6054257', 'G', ['A', ''], 29.0, (True, False, False), 2, True),
#       ('20', 17330, '.', 'T', ['A', ''], 3.0, (False, True, False), 2, True),
#       ('20', 1110696, 'rs6040355', 'A', ['G', 'T'], 67.0, (True, False, False), 3, True),
#       ('20', 1230237, '.', 'T', ['.', ''], 47.0, (True, False, False), 2, False),
#       ('20', 1234567, 'microsat1', 'G', ['GA', 'GAC'], 50.0, (True, False, False), 3, False),
#       ('20', 1235237, '.', 'T', ['.', ''], 0.0, (False, False, False), 2, False),
#       ('X', 10, 'rsTest', 'AC', ['A', 'ATG'], 10.0, (True, False, False), 3, False)], 
#      dtype=[('CHROM', '|S12'), ('POS', '<i4'), ('ID', '|S12'), ('REF', '|S12'), ('ALT', '|S12', (2,)), ('QUAL', '<f4'), ('FILTER', [('PASS', '|b1'), ('q10', '|b1'), ('s50', '|b1')]), ('num_alleles', '|u1'), ('is_snp', '|b1')])


def test_variants_region():
    a = variants('sample.vcf.gz', region='20')
    eq_(6, len(a))
    
    
def test_variants_count():
    a = variants('sample.vcf', count=3)
    eq_(3, len(a))
    
    
def test_variants_exclude_fields():
    a = variants('sample.vcf', exclude_fields=['ID', 'FILTER'])
    assert 'CHROM' in a.dtype.names
    assert 'ID' not in a.dtype.names
    assert 'FILTER' not in a.dtype.names
    
    
def test_info():
    a = info('sample.vcf', arities={'AC': 2})
    print repr(a)
    eq_(3, a[2]['NS'])
    eq_(.5, a[2]['AF'])
    eq_(True, a[2]['DB'])
    eq_((3, 1), tuple(a[6]['AC']))

#array([(0, 0, [0, 0], 0, 0.0, '', False, False),
#       (0, 0, [0, 0], 0, 0.0, '', False, False),
#       (3, 0, [0, 0], 14, 0.5, '', True, True),
#       (3, 0, [0, 0], 11, 0.017000000923871994, '', False, False),
#       (2, 0, [0, 0], 10, 0.3330000042915344, 'T', True, False),
#       (3, 0, [0, 0], 13, 0.0, 'T', False, False),
#       (3, 6, [3, 1], 9, 0.0, 'G', False, False),
#       (0, 0, [0, 0], 0, 0.0, '', False, False),
#       (0, 0, [0, 0], 0, 0.0, '', False, False)], 
#      dtype=[('NS', '<i4'), ('AN', '<i4'), ('AC', '<i4', (2,)), ('DP', '<i4'), ('AF', '<f4'), ('AA', '|S12'), ('DB', '|b1'), ('H2', '|b1')])


def test_calldata():
    a = calldata('sample.vcf')
    print repr(a)
    eq_('0|0', a[0]['NA00001']['GT'])
    eq_(True, a[0]['NA00001']['is_called'])
    eq_(True, a[0]['NA00001']['is_phased'])
    eq_((0, 0), tuple(a[0]['NA00001']['genotype']))
    eq_((10, 10), tuple(a[0]['NA00001']['HQ']))

#>>> a['NA00001']
#array([(True, True, [0, 0], '0|0', 0, 0, [10, 10]),
#       (True, True, [0, 0], '0|0', 0, 0, [10, 10]),
#       (True, True, [0, 0], '0|0', 48, 1, [51, 51]),
#       (True, True, [0, 0], '0|0', 49, 3, [58, 50]),
#       (True, True, [1, 2], '1|2', 21, 6, [23, 27]),
#       (True, True, [0, 0], '0|0', 54, 0, [56, 60]),
#       (True, False, [0, 1], '0/1', 0, 4, [0, 0]),
#       (True, False, [0, 0], '0/0', 0, 0, [0, 0]),
#       (True, False, [0, -1], '0', 0, 0, [0, 0])], 
#      dtype=[('is_called', '|b1'), ('is_phased', '|b1'), ('genotype', '|i1', (2,)), ('GT', '|S3'), ('GQ', '|u1'), ('DP', '<u2'), ('HQ', '<i4', (2,))])
    