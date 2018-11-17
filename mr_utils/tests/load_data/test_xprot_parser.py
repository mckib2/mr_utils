import unittest
from mr_utils.load_data.xprot_parser import XProtParser
from mr_utils.test_data import XProtParserTest

class XProtParserTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_sample(self):
        sample = XProtParserTest.sample_xprot()
        # print(sample)
        parser = XProtParser()
        parser.parse(sample)


if __name__ == '__main__':
    unittest.main()
