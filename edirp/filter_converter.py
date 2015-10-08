# '''This class intended to open the zipped files, filter them, and convert to the expected output format'''
import os

from file_downloader import FileDownloader
from pdb_file import PDBFile


class FilterConverter:
    DATA_SET = 'data_set'
    DEFAULT_MIN_RESOLUTION = 3.0
    DEFAULT_MIN_CHAIN_LENGTH = 30
    DEFAULT_ATOM_TYPE = 'P'

    def __init__(self, **kwargs):
        try:
            working_dir = kwargs['working_dir']
        except KeyError:
            raise Exception('You should specify the working directory!')

        self.input_path = os.path.join(working_dir, FileDownloader.TARGET_FOLDER)
        self.output_path = os.path.join(working_dir, self.DATA_SET)
        if not os.path.isdir(self.output_path):
            os.makedirs(self.output_path)

        self.min_resolution = kwargs.get('min_resolution') or self.DEFAULT_MIN_RESOLUTION
        self.min_chain_length = kwargs.get('min_chain_length') or self.DEFAULT_MIN_CHAIN_LENGTH
        self.atom_type = kwargs.get('atom_type') or self.DEFAULT_ATOM_TYPE

    def filter_and_convert(self):
        file_names = self.list_zipped_files()

        number_of_chains = 0
        for file_name in file_names:
            pdb_file = PDBFile.from_zip(file_name, self.atom_type)
            if pdb_file.has_better_resolution(self.min_resolution):
                chains = pdb_file.get_chains(self.min_chain_length)
                number_of_chains += len(chains)
                for chain in chains:
                    chain.write_to_file(self.output_path, pdb_file)
        print 'Found {number_of_chains} chains matching the criteria'.format(number_of_chains=number_of_chains)

    def list_zipped_files(self):
        return [os.path.join(self.input_path, zip_file_name) for zip_file_name in os.listdir(self.input_path)]
