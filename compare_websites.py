# coding:utf-8
import unittest

import slugify
from PIL import Image, ImageChops

from StringIO import StringIO
from selenium import webdriver

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

    def setUp(self):
        """Open a new browser for each test."""
        super(TestTemplate, self).setUp()

        profile = webdriver.ChromeOptions()
        options = {
            "intl": {
                "accept_languages": "en-US,en"
            }
        }
        profile.add_experimental_option("prefs", options)
        self.driver = webdriver.Chrome(chrome_options=profile)

        self.driver.set_window_size(1280, 1024)  # <= tweak this as needed

    def tearDown(self):
        self.driver.close()

    def assertImageEqual(self, img1, img2, msg=None, threshold=None,
                         save_diff_file=None):
        # adapted from http://stackoverflow.com/questions/16720594/
        a = Image.open(StringIO(img1))
        b = Image.open(StringIO(img2))
        diff = ImageChops.difference(a, b)
        diff = diff.convert('L')
        diff = diff.point(TestTemplate.__point_table)
        c = diff.convert('RGB')
        c.paste(b, mask=diff)

        # test if the result contains any pixel
        bbox = c.getbbox()
        if bbox:
            if save_diff_file:
                c.save(save_diff_file)

            if threshold:
                # from http://codereview.stackexchange.com/questions/55902
                n_pixels_diff = sum(c.crop(bbox)
                                    .point(lambda x: 255 if x else 0)
                                    .convert("L")
                                    .point(bool)
                                    .getdata())

                if n_pixels_diff >= threshold:
                    raise self.fail(self._formatMessage(msg, 'images are different (%s pixels >= %s)' % (n_pixels_diff, threshold)))
                else:
                    return

            raise self.fail(self._formatMessage(msg, 'images are different'))

    def test_compare_domains(self):
        domains = self._test_kwargs['domains']
        if len(domains) != 2:
            raise self.failureException('there must be 2 domains')

        path = self._test_kwargs['path']

        url1 = domains[0] + path
        url2 = domains[1] + path

        self.driver.get(url1)
        img1 = self.driver.get_screenshot_as_png()

        # NB: if necessary, one could close and re-init the driver in between

        self.driver.get(url2)
        img2 = self.driver.get_screenshot_as_png()

        diff_file = 'error_%s.png' % slugify.slugify(path)
        self.assertImageEqual(img1, img2,
                              msg='%s and %s are different' % (url1, url2),
                              # threshold=10,
                              save_diff_file=diff_file)

if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTest(TestTemplate(domains=('https://test-infoscience.epfl.ch',
                                        'https://infoscience.epfl.ch'),
                               path='/record/221397'))
    # ... call addTest(TestTemplate(...)) with as many paths as needed ...

    unittest.TextTestRunner().run(suite)
