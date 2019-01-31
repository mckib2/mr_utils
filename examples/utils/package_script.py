'''Demonstrate how to package a mr_util script.'''

import os

from mr_utils.utils import package_script
from mr_utils.definitions import ROOT_DIR


if __name__ == '__main__':

    filename = os.path.join(
        ROOT_DIR, 'mr_utils', 'recon', 'ssfp', 'gs_recon.py')

    val = package_script(filename, existing_modules=['numpy', 'scipy', 'h5py'])
    print(val)
