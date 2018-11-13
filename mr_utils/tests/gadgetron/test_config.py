import unittest
import numpy as np
from mr_utils.gadgetron.configs import GadgetronConfig,default_config,grappa_cpu_config
from mr_utils.gadgetron import client
from mr_utils.test_data import GadgetronClient
from mr_utils.test_data import GadgetronTestConfig
from mr_utils import view
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
        config = default_config()
        truth = GadgetronTestConfig.default_config()
        res = len(main.diff_texts(truth.encode(),config.tostring().encode()))
        self.assertTrue(res == 0)

    def test_use_default_config(self):
        # Give the filename of raw data to the client
        filename = GadgetronClient.raw_input_filename()

        # Send gadgetron the local default configuration file
        config = default_config()
        # print(config)
        # data,header = client(filename,config_local=config.get_filename())
        data,header = client(filename,config_local=config.tostring())

        # Make sure the output is the same as when h5 is given
        true_output_data = GadgetronClient.true_output_data()
        assert(np.allclose(data,true_output_data))

    def test_use_grappa_cpu_config(self):
        filename = GadgetronClient.grappa_input_filename()
        config = grappa_cpu_config()
        data,header = client(filename,config_local=config.tostring())
        # data,header = client(filename,config='grappa_cpu.xml')
        # np.save('true_output_data_grappa_cpu.npy',data)
        true_output_data = GadgetronClient.true_output_data_grappa_cpu()
        assert(np.allclose(data,true_output_data))

if __name__ == '__main__':
    unittest.main()
