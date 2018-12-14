import unittest
from mr_utils.gadgetron import client
from mr_utils.gadgetron import GadgetronConfig
from mr_utils.test_data import GadgetronClient
from mr_utils import view

class GadgetronGSRecon(unittest.TestCase):

    def setUp(self):
        self.filename = GadgetronClient.grappa_input_filename()

    def test_gadgetron_grappa_coil_output(self):

        config = GadgetronConfig()
        config.add_reader('1008','GadgetIsmrmrdAcquisitionMessageReader')
        config.add_reader('1026','GadgetIsmrmrdWaveformMessageReader')
        config.add_writer('1022','MRIImageWriter')
        config.add_gadget('RemoveROOversampling')
        config.add_gadget('Grappa',props=[
            ('target_coils','8'),
            ('use_gpu','false'),
            ('uncombined_channels','1,2,3,4,5,6,7,8,9,10,11,12')
        ])
        config.add_gadget('GrappaUnmixing')
        config.add_gadget('Extract',props=[
            ('extract_magnitude','false')
            ('extract_real','true'),
            ('extract_imag','true')
        ])
        config.add_gadget('ImageFinish')

        data,header = client(self.filename,config_local=config.tostring())
        data = data[0,...] + 1j*data[1,...]
        view(data,montage_axis=0)

if __name__ == '__main__':
    unittest.main()
