import json

from . import defaults
from .edirp_level_ranges import EdirpLevelRanges


class EdirpConfigParser:
    FIX_VALUES = ('working_dir', 'min_resolution', 'min_chain_length', 'edirp_level_ranges_file_path',)

    def __init__(self, **kwargs):
        try:
            config_data = self.config_data_from_json(defaults.DEFAULT_EDIRP_CONFIG_FILE_PATH)
            for key, value in kwargs.items():
                if value is not None:
                    config_data[key] = value
        except IOError:
            config_data = kwargs

        # general config
        self.working_dir = config_data.get('working_dir') or defaults.DEFAULT_WORKING_DIR

        # pull configs
        self.max_number = config_data.get('max_number')

        # data set filter configs
        self.min_resolution = config_data.get('min_resolution') or defaults.DEFAULT_MIN_RESOLUTION
        self.min_chain_length = config_data.get('min_chain_length') or defaults.DEFAULT_MIN_CHAIN_LENGTH
        self.atom_type = config_data.get('atom_type') or defaults.DEFAULT_ATOM_TYPE

        # for edirp conversion
        edirp_level_ranges_file_path = config_data.get('edirp_level_ranges_file_path') or defaults.DEFAULT_EDIRP_LEVEL_RANGES_FILE_PATH
        self.edirp_level_ranges = EdirpLevelRanges.from_json(edirp_level_ranges_file_path)

    @staticmethod
    def create_config_interactively():
        print 'Welcome to the interactive configuration tool'
        working_dir = raw_input('Please enter the working directory. DEFAULT: {home}\n'
                                '(The temporary folders and all the data will be stored under this location)\n'
                                .format(home=defaults.DEFAULT_WORKING_DIR))

        min_resolution = raw_input('Please enter the minimum accepted resolution in Angstroms DEFAULT: {resolution}\n'
                                   '(The PDB structures will be filtered based on this number)\n'
                                   .format(resolution=defaults.DEFAULT_MIN_RESOLUTION))

        min_chain_length = raw_input('Please enter the minimum accepted chain length. DEFAULT: {chain_length}\n'
                                     '(The PDB structures will be filtered based on this number)\n'
                                     .format(chain_length=defaults.DEFAULT_MIN_CHAIN_LENGTH))

        atom_type = raw_input('Please enter the atom type you want to filter on. DEFAULT: {atom_type}\n'
                              'for further info about atom type please check your files eg. C1, O2..\n'
                              .format(atom_type=defaults.DEFAULT_ATOM_TYPE))

        edirp_level_ranges_file_path = raw_input('Please enter the path to the json config file containing the EDIRP\n'
                                                 'level ranges. DEFAULT: {path}\n'
                                                 .format(path=defaults.DEFAULT_EDIRP_LEVEL_RANGES_FILE_PATH))

        config_file_path = raw_input('Please enter the path of the configuration file. DEFAULT: {config_path}\n'
                                     .format(config_path=defaults.DEFAULT_EDIRP_CONFIG_FILE_PATH))

        try:
            min_resolution = float(min_resolution.strip())
        except ValueError:
            min_resolution = None

        try:
            min_chain_length = int(min_chain_length.strip())
        except ValueError:
            min_chain_length = None

        data = {
            'working_dir': working_dir or defaults.DEFAULT_WORKING_DIR,
            'min_resolution': min_resolution or defaults.DEFAULT_MIN_RESOLUTION,
            'min_chain_length': min_chain_length or defaults.DEFAULT_MIN_CHAIN_LENGTH,
            'atom_type': atom_type or defaults.DEFAULT_ATOM_TYPE,
            'edirp_level_ranges_file_path': edirp_level_ranges_file_path or defaults.DEFAULT_EDIRP_LEVEL_RANGES_FILE_PATH,
        }

        config_file_path = config_file_path or defaults.DEFAULT_EDIRP_CONFIG_FILE_PATH

        EdirpConfigParser(**data).to_json(config_file_path)

    def to_json(self, json_file_path):
        with open(json_file_path, 'w') as json_file:
            json.dump({
                'working_dir': self.working_dir,
                'max_number': self.max_number,
                'min_resolution': self.min_resolution,
                'min_chain_length': self.min_chain_length,
                'atom_type': self.atom_type,
            }, json_file)

    @staticmethod
    def config_data_from_json(json_file_path):
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
            return json_data

    def get_config(self):
        return {
            'working_dir': self.working_dir,
            'max_number': self.max_number,
            'min_resolution': self.min_resolution,
            'min_chain_length': self.min_chain_length,
            'atom_type': self.atom_type,
            'edirp_level_ranges': self.edirp_level_ranges,
        }
