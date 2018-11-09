import unittest
from mr_utils.gadgetron.config import GadgetronConfig
from mr_utils.test_data import GadgetronTestConfig
from xml.etree import ElementTree as ET
from xmldiff import main

class GadgetronConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.config = GadgetronConfig()

    def test_create_xml(self):
        self.config.add_reader(1008,'GadgetIsmrmrdAcquisitionMessageReader')
        self.config.add_writer(1004,'MRIImageWriterCPLX')
        self.config.add_writer(1005,'MRIImageWriterFLOAT')
        self.config.add_writer(1006,'MRIImageWriterUSHORT')
        self.config.add_gadget('Acc','AccumulatorGadget')
        self.config.add_gadget('FFT')
        self.config.add_gadget('Extract')
        self.config.add_gadget('ImageFinishFLOAT','ImageFinishGadgetFLOAT')
        # self.config.print()

    def test_create_default_config(self):
        self.config.add_reader('1008','GadgetIsmrmrdAcquisitionMessageReader')
        self.config.add_reader('1026','GadgetIsmrmrdWaveformMessageReader')
        self.config.add_writer('1022','MRIImageWriter')
        self.config.add_gadget('RemoveROOversampling')
        self.config.add_gadget('AccTrig','AcquisitionAccumulateTriggerGadget',props=[
            ('trigger_dimension','repetition'),
            ('sorting_dimension','slice')
        ])
        self.config.add_gadget('Buff','BucketToBufferGadget',props=[
            ('N_dimension',''),
            ('S_dimension',''),
            ('split_slices','true')
        ])
        self.config.add_gadget('SimpleRecon')
        self.config.add_gadget('ImageArraySplit')
        self.config.add_gadget('Extract')
        self.config.add_gadget('ImageFinish')
        # self.config.print()

        truth = GadgetronTestConfig.default_config()
        res = len(main.diff_texts(truth.encode(),self.config.tostring().encode()))
        self.assertTrue(res == 0)

if __name__ == '__main__':
    unittest.main()
