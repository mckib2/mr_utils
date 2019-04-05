'''Remote Gadgetron execution of custom Python Gadget.

Example demonstrating how to use the Gadgetron client to send a
python Gadget to the remote Gadgetron server and use it in a Gadget chain.

The idea is to "bundle" all of the dependencies of the script
together so that there is no extra setup/installation step before the
remote machine is able to run the custom python Gadget.
'''

import os

from mr_utils.gadgetron import client
from mr_utils.gadgetron import GadgetronConfig
from mr_utils.test_data import load_test_data
from mr_utils.definitions import ROOT_DIR
from mr_utils import view

if __name__ == '__main__':

    # Load in a numerical phantom to play around with
    path = 'mr_utils/test_data/tests/gadgetron/client/'
    file = 'input.h5'
    load_test_data(path, [file], do_return=False)
    data = '%s/%s' % (path, file)

    # Make a config
    script_dir = 'tmp/'
    default_dir = ''
    config = GadgetronConfig()
    config.add_reader('1008', 'GadgetIsmrmrdAcquisitionMessageReader')
    config.add_reader('1026', 'GadgetIsmrmrdWaveformMessageReader')
    config.add_writer('1022', 'MRIImageWriter')
    config.add_gadget('RemoveOversamplingPython', 'PythonGadget', props=[
        ('python_path', default_dir),
        ('python_module', 'remove_2x_oversampling'),
        ('python_class', 'Remove2xOversampling'),
    ])
    config.add_gadget('AccReconPython', 'PythonGadget', props=[
        ('python_path', default_dir),
        ('python_module', 'accumulate_and_recon'),
        ('python_class', 'AccumulateAndRecon'),
    ])
    config.add_gadget('CoilCombinePython', 'PythonGadget', props=[
        ('python_path', script_dir),
        ('python_module', 'rms_coil_combine'),
        ('python_class', 'RMSCoilCombine'),
    ])
    config.add_gadget('Extract')
    config.add_gadget('AutoScale')
    config.add_gadget('FloatToShort', 'FloatToUShortGadget')
    config.add_gadget('ImageFinish')

    # Get the path to the script we want to send over
    script_path = os.path.join(
        ROOT_DIR, 'mr_utils', 'gadgetron', 'gadgets', 'rms_coil_combine.py')

    # from mr_utils.utils import package_script
    # test = ROOT_DIR + '/mr_utils/utils/mi_ssfp.py'
    # print(package_script(test, existing_modules=['numpy', 'scipy']))

    im, hdr = client(
        data,
        config_local=config.tostring(),
        script=script_path,
        script_dir=script_dir,
        verbose=True)
    view(im)
