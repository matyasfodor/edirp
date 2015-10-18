import os

DEFAULT_PROJECT_DIR = '{home}/workspace/edirp/'.format(home=os.environ.get('HOME'))

DEFAULT_WORKING_DIR = os.path.join(DEFAULT_PROJECT_DIR, 'data/')

DEFAULT_EDIRP_CONFIG_FILE_PATH = os.path.join(DEFAULT_PROJECT_DIR, 'edirp_config.json')
DEFAULT_EDIRP_LEVEL_RANGES_FILE_PATH = os.path.join(DEFAULT_PROJECT_DIR, 'edirp_level_ranges.json')

DEFAULT_MIN_RESOLUTION = 3.0
DEFAULT_MIN_CHAIN_LENGTH = 30
DEFAULT_ATOM_TYPE = 'P'
