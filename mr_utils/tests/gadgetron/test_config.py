import unittest
import numpy as np
from mr_utils.gadgetron import GadgetronConfig
from mr_utils.gadgetron import configs
from mr_utils.gadgetron import client
from mr_utils.test_data import GadgetronClient
from mr_utils.test_data import GadgetronTestConfig
from mr_utils import view
from xmldiff import main

class GadgetronConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.config = GadgetronConfig()
        self.filename = GadgetronClient.grappa_input_filename()

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
        config = configs.default()
        truth = GadgetronTestConfig.default_config()
        res = len(main.diff_texts(truth.encode(),config.tostring().encode()))
        self.assertTrue(res == 0)

    def test_use_default_config(self):
        # Give the filename of raw data to the client
        filename = GadgetronClient.raw_input_filename()

        # Send gadgetron the local default configuration file
        config = configs.default()
        # print(config)
        # data,header = client(filename,config_local=config.get_filename())
        data,header = client(filename,config_local=config.tostring())

        # Make sure the output is the same as when h5 is given
        true_output_data = GadgetronClient.true_output_data()
        self.assertTrue(np.allclose(data,true_output_data))

    def test_use_grappa_cpu_config(self):
        config = configs.grappa_cpu()
        data,header = client(self.filename,config_local=config.tostring())
        data_true,header_true = client(self.filename,config='grappa_cpu.xml')
        self.assertTrue(np.allclose(data,data_true))

    def test_use_grappa_float_cpu_config(self):
        config = configs.grappa_float_cpu()
        data,header = client(self.filename,config_local=config.tostring())
        data_true,header_true = client(self.filename,config='grappa_float_cpu.xml')
        self.assertTrue(np.allclose(data,data_true))

    def test_use_grappa_unoptimized_cpu_config(self):
        config = configs.grappa_unoptimized_cpu()
        data,header = client(self.filename,config_local=config.tostring())
        data_true,header_true = client(self.filename,config='grappa_unoptimized.xml')
        self.assertTrue(np.allclose(data,data_true))

    def test_use_grappa_unoptimized_float_cpu_config(self):
        config = configs.grappa_unoptimized_float_cpu()
        data,header = client(self.filename,config_local=config.tostring())
        data_true,header_true = client(self.filename,config='grappa_unoptimized_float.xml')
        self.assertTrue(np.allclose(data,data_true))

    def test_use_distributed_default_config(self):
        config = configs.distributed_default()
        data,header = client(self.filename,config_local=config.tostring())
        data_true,header_true = client(self.filename,config='distributed_default.xml')
        self.assertTrue(np.allclose(data,data_true))

    def test_use_distributed_image_default_config(self):
        config = configs.distributed_image_default()
        data,header = client(self.filename,config_local=config.tostring())
        data_true,header_true = client(self.filename,config='distributed_image_default.xml')
        self.assertTrue(np.allclose(data,data_true))


if __name__ == '__main__':
    unittest.main()
