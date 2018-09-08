from distutils.core import setup
from setuptools import find_packages

setup(
    name='mr_utils',
    version='0.0.0',
    author='Nicholas McKibben',
    author_email='nicholas@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/mckib2/mr_utils',
    license='',
    description='Collection of MR utilities.',
    long_description='', #open('README.rst').read(),
    install_requires=[
        "numpy>=1.14.1",
        "scipy>=1.0.0",
        "h5py>=2.7.1",
        "rawdatarinator>=0.1.9",
        "matplotlib>=2.1.1"
    ],
    python_requires='>=3.6',
)
