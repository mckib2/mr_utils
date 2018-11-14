import os

# point to the directory right above us where profiles.config is located
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BART_PATH = os.environ['TOOLBOX_PATH'] + '/python'
# if not os.path.isfile(BART_PATH):
#     BART_PATH = None
