import unittest
import ucbreq
from collections import OrderedDict

class LoadTest(unittest.TestCase):
    def test_loads_default(self):
        d = OrderedDict()
        d['foo'] = 'bar'
        d['baz'] = ['alpha', 'beta', 'gamma']
        d['delta'] = 'eins'
        d['zwei'] = ['drei', 'vier']
        self.assertEqual(
            d,
            ucbreq.loads(
                "foo|bar\nbaz_5|alpha\nbaz_6|beta\nbaz_7|gamma\ndelta|eins\nzwei_5|drei\nzwei_6|vier\n",
                dict_class=OrderedDict,
                ))
        self.assertEqual(
            d,
            ucbreq.loads(
                "foo=bar\nbaz_1=alpha\nbaz_2=beta\nbaz_3=gamma\ndelta=eins\nzwei_1=drei\nzwei_2=vier\n",
                dict_class=OrderedDict,
                separator='=',
                ))
        self.assertEqual(
            d,
            ucbreq.loads(
                "foo|bar\nbaz,1|alpha\nbaz,2|beta\nbaz,3|gamma\ndelta|eins\nzwei,1|drei\nzwei,2|vier\n",
                dict_class=OrderedDict,
                index_separator=',',
                ))
        self.assertEqual(
            d,
            ucbreq.loads(
                "foo|bar\nbaz_1|alpha\ndelta|eins\nbaz_3|gamma\nzwei_1|vier\nbaz_2|beta\nzwei|drei\n",
                dict_class=OrderedDict,
                ))

    def test_keep_originals(self):
        d = OrderedDict()
        d['foo'] = 'bar'
        d['baz'] = ['alpha', 'beta', 'gamma']
        d['baz_5'] = 'alpha'
        d['baz_6'] = 'beta'
        d['baz_7'] = 'gamma'
        d['delta'] = 'eins'
        d['zwei'] = ['drei', 'vier']
        d['zwei_5'] = 'drei'
        d['zwei_6'] = 'vier'

        self.assertEqual(
            d,
            ucbreq.loads(
                "foo|bar\nbaz_5|alpha\nbaz_6|beta\nbaz_7|gamma\ndelta|eins\nzwei_5|drei\nzwei_6|vier\n",
                dict_class=OrderedDict,
                keep_originals=True,
                ))
