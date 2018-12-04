from mr_utils.gadgetron import client
from mr_utils.test_data import BSSFPGrappa
from mr_utils import view

if __name__ == '__main__':

    # Get sample data, bssfp, phase-cycle=0, R=2
    filename = BSSFPGrappa.pc0_r2()

    # Look at before sent to gadgetron
    view(filename,fft=True,load_opts={'use':'rdi'},coil_combine_axis=-1,fft_axes=(0,1))

    # Now send it to Gadgetron and look at the result
    data,header = client(filename,config='grappa.xml')
    view(data)
