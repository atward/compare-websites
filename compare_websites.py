# coding:utf-8
import unittest

import urllib.request

__author__ = "Charles François Rey"
__copyright__ = "Copyright (c) 2017 Charles François Rey"
__license__ = "MIT"
__version__ = "0.1.0"
__status__ = "Prototype"


class TestTemplate(unittest.TestCase):
    __point_table = ([0] + ([255] * 255))

    def __init__(self, **kwargs):
        super(TestTemplate, self).__init__('test_compare_domains')
        self._test_kwargs = kwargs

    @staticmethod
    def get(url):
        return urllib.request.urlopen(url).read()

    def test_compare_domains(self):
        domains = self._test_kwargs['domains']
        if len(domains) != 2:
            raise self.failureException('there must be 2 domains')

        path = self._test_kwargs['path']

        url1 = domains[0] + path
        url2 = domains[1] + path

        res1 = self.get(url1)
        res2 = self.get(url2)

        self.assertEqual(res1, res2, msg='%s and %s are different' % (url1, url2))

if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTest(TestTemplate(domains=('http://example.com', 'http://www.example.com'), path='/'))
    # ... call addTest(TestTemplate(...)) with as many paths as needed ...

    unittest.TextTestRunner().run(suite)
