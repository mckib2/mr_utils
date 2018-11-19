import os
from distutils.spawn import find_executable

# point to the directory right above us where profiles.config is located
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Check for BART
if not os.path.isdir(os.environ['TOOLBOX_PATH'] + '/python'):
    BART_PATH = None
else:
    BART_PATH = os.environ['TOOLBOX_PATH'] + '/python'

# Check for siemens_to_ismrmrd
if find_executable('siemens_to_ismrmrd') is not None:
    SIEMENS_TO_ISMRMRD_INSTALLED = True
else:
    SIEMENS_TO_ISMRMRD_INSTALLED = False
