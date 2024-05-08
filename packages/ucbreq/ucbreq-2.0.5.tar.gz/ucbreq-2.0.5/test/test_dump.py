import unittest
import ucbreq
from collections import OrderedDict

class DumpTest(unittest.TestCase):
    def test_dumps_default(self):
        d = OrderedDict()
        d['foo'] = 'bar'
        d['baz'] = ('alpha', 'beta', 'gamma')
        d['delta'] = 'eins'
        d['zwei'] = ('drei', 'vier')
        self.assertEqual(ucbreq.dumps(d), "foo|bar\nbaz_1|alpha\nbaz_2|beta\nbaz_3|gamma\ndelta|eins\nzwei_1|drei\nzwei_2|vier\n")
        self.assertEqual(ucbreq.dumps(d, startindex=5), "foo|bar\nbaz_5|alpha\nbaz_6|beta\nbaz_7|gamma\ndelta|eins\nzwei_5|drei\nzwei_6|vier\n")
        self.assertEqual(ucbreq.dumps(d, separator='='), "foo=bar\nbaz_1=alpha\nbaz_2=beta\nbaz_3=gamma\ndelta=eins\nzwei_1=drei\nzwei_2=vier\n")
        self.assertEqual(ucbreq.dumps(d, index_separator=','), "foo|bar\nbaz,1|alpha\nbaz,2|beta\nbaz,3|gamma\ndelta|eins\nzwei,1|drei\nzwei,2|vier\n")

        with self.assertRaises(ValueError):
            ucbreq.dumps(d, startindex=-1)
