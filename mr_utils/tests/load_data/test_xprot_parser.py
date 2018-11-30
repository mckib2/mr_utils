import unittest
from mr_utils.load_data.xprot_parser import XProtParser
from mr_utils.test_data import XProtParserTest
import json
from mr_utils.load_data.parser.infoparser import InfoParser
import xmltodict

class XProtParserTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_sample(self):
        sample = XProtParserTest.full_sample_xprot()
        # # print(sample)
        # parser = XProtParser()
        # parser.parse(sample)
        # res = parser.structure['XProtocol']['Dependency']
        # print(json.dumps(res,indent=2))

        # plongs = parser.structure['XProtocol']['Params']['ParamArray']
        # for p in plongs:
        #     if '\"RealDwellTime\"' in p:
        #         # if p['parent'] == 'ParamMap."sEFISPEC"':
        #         #     ans = [ int(x) for x in p['\"alFree\"'] ]
        #         #     break
        #         print(p['\"RealDwellTime\"'][0]['Default'])
        # print(ans)

        # res = parser.structure['XProtocol']['Dependency']
        # print(json.dumps(parser.structure,indent=2))

        rdiParser = InfoParser()
        doc_root = xmltodict.parse(rdiParser.raw2xml(sample))['doc_root']
        res = [ int(x) for x in doc_root['ParamMap_sWiPMemBlock']['ParamLong_alFree']['value'] ]
        res = [ float(x) for x in doc_root['ParamMap_sWiPMemBlock']['ParamDouble_adFree']['value'][1:] ]
        res = [ int(x) for x in doc_root['ParamMap_sRXSPEC']['ParamLong_alDwellTime']['value'] ]
        res = [ int(doc_root['ParamMap_sKSpace']['ParamLong_ucTrajectory']['value']) ]
        res = [ int(doc_root['ParamMap_YAPS']['ParamLong_iMaxNoOfRxChannels']['value']) ]
        res = [ int(doc_root['ParamMap_sKSpace']['ParamLong_lPhaseEncodingLines']['value']) ]
        res = [ int(doc_root['ParamMap_YAPS']['ParamLong_iNoOfFourierLines']['value']) ]
        res = doc_root['ParamMap_YAPS']['ParamLong_lFirstFourierLine']

        print(json.dumps(res,indent=2))

if __name__ == '__main__':
    unittest.main()
