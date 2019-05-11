'''Setup.py.

Installation:
    Say you want to use this package in one of your python scripts. You can
    install it using pip like so:

        git clone https://github.com/mckib2/mr_utils
        cd mr_utils
        pip3 install -e ./

    You'll need to manually install the ismrmrd-python-tools as it's currently
    not available on PyPi. You can find it here:
        https://github.com/ismrmrd/ismrmrd-python-tools.git
'''

from distutils.core import setup
from setuptools import find_packages

setup(
    name='mr_utils',
    version='0.0.0',
    author='Nicholas McKibben',
    author_email='nicholas.bgp@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/mckib2/mr_utils',
    license='',
    description='Collection of MR utilities.',
    long_description=open('README.rst').read(),
    install_requires=[
        "numpy>=1.16.2",
        "scipy>=1.2.1",
        "h5py>=2.9.0",
        "rawdatarinator>=0.1.9",
        "matplotlib>=3.0.3",
        "scikit-image>=0.14.2",
        "scikit-learn>=0.20.3",
        "xmldiff>=2.3",
        "tqdm>=4.31.1",
        "paramiko>=2.4.2",
        "ismrmrd>=1.4.0",
        "xmltodict>=0.12.0",
        "nibabel>=2.3.3",
        "PyWavelets>=1.0.2",
        "prox-tv>=3.3.0"
    ],
    python_requires='>=3.6',
)
