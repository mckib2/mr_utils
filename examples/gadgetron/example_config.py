'''Example of how to programmatically generate a config file.'''

from mr_utils.gadgetron import GadgetronConfig

if __name__ == '__main__':

    config = GadgetronConfig()
    config.add_reader(1008, 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_writer(1004, 'MRIImageWriterCPLX')
    config.add_writer(1005, 'MRIImageWriterFLOAT')
    config.add_writer(1006, 'MRIImageWriterUSHORT')
    config.add_gadget('Acc', 'AccumulatorGadget')
    config.add_gadget('FFT')
    config.add_gadget('Extract')
    config.add_gadget('ImageFinishFLOAT', 'ImageFinishGadgetFLOAT')
    print(config.tostring())
