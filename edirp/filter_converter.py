# '''This class intended to open the zipped files, filter them, and convert to the expected output format'''
import os

from .edirp_config_parser import EdirpConfigParser
from .file_downloader import FileDownloader
from .pdb_file import PDBFile


class FilterConverter:
    DATA_SET = 'data_set'
    DATA_SET_EDIRP = 'data_set_edirp'

    def __init__(self, **kwargs):
        config = EdirpConfigParser(**kwargs).get_config()
        working_dir = config['working_dir']
        if not os.path.isdir(working_dir):
            os.makedirs(working_dir)

        self.input_path = os.path.join(working_dir, FileDownloader.TARGET_FOLDER)
        self.output_path_json = os.path.join(working_dir, self.DATA_SET)
        if not os.path.isdir(self.output_path_json):
            os.makedirs(self.output_path_json)

        self.output_path_edirp_json = os.path.join(working_dir, self.DATA_SET_EDIRP)
        if not os.path.isdir(self.output_path_edirp_json):
            os.makedirs(self.output_path_edirp_json)

        self.min_resolution = config['min_resolution']
        self.min_chain_length = config['min_chain_length']
        self.atom_type = config['atom_type']

    def filter_and_convert_to_json(self):
        chains = self._extract_filtered_chains(self)

        print 'Found {number_of_chains} chains matching the criteria'.format(number_of_chains=len(chains))

        for chain in chains:
                chain.write_to_file(self.output_path_json)

    def filter_and_convert_to_edirp(self):
        chains = self._extract_filtered_chains(self)

        print 'Found {number_of_chains} chains matching the criteria'.format(number_of_chains=len(chains))

        for chain in chains:
            chain.write_to_edirp_file(self.output_path_edirp_json)

    def _extract_filtered_chains(self):
        file_names = self.list_zipped_files()
        chains = []

        for file_name in file_names:
            pdb_file = PDBFile.from_zip(file_name, self.atom_type)
            if pdb_file.has_better_resolution(self.min_resolution):
                chains += pdb_file.get_chains(self.min_chain_length)

        return chains

    def list_zipped_files(self):
        return [os.path.join(self.input_path, zip_file_name) for zip_file_name in os.listdir(self.input_path)]
