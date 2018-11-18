import unittest
from mr_utils.load_data.xprot_parser import XProtParser
from mr_utils.test_data import XProtParserTest
import json

class XProtParserTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_sample(self):
        sample = XProtParserTest.full_sample_xprot()
        # print(sample)
        parser = XProtParser()
        parser.parse(sample)

        plongs = parser.structure['XProtocol']['Params']['ParamArray']
        for p in plongs:
            if '\"RealDwellTime\"' in p:
                # if p['parent'] == 'ParamMap."sEFISPEC"':
                #     ans = [ int(x) for x in p['\"alFree\"'] ]
                #     break
                print(p['\"RealDwellTime\"'][0]['Default'])
        # print(ans)

        # res = parser.structure['XProtocol']['Dependency']
        # print(json.dumps(res,indent=2))



if __name__ == '__main__':
    unittest.main()
