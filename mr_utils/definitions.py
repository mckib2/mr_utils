'''Provide definitions of paths for root andapplications if they exist.'''

import os
from distutils.spawn import find_executable

# point to the directory right above us where profiles.config is located
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# host where test data is accessible
TEST_DATA_HOST = 'https://birly.groups.et.byu.net/'

# Check for BART
try:
    if not os.path.isdir(os.environ['TOOLBOX_PATH'] + '/python'):
        BART_PATH = None
    else:
        BART_PATH = os.environ['TOOLBOX_PATH'] + '/python'
except KeyError:
    BART_PATH = None

# Check for siemens_to_ismrmrd
SIEMENS_TO_ISMRMRD_INSTALLED = find_executable(
    'siemens_to_ismrmrd') is not None
