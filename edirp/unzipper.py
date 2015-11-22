import gzip
import os

from file_downloader import FileDownloader


class Unzipper:
    UNZIPPED_PATH = 'pdbs'
    ZIP_EXTENSION = '.ent.gz'
    PDB_EXTENSION = '.pdb'

    def __init__(self, working_dir):
        self.input_path = os.path.join(working_dir, FileDownloader.TARGET_FOLDER)
        self.output_path = os.path.join(working_dir, self.UNZIPPED_PATH)

        if not os.path.isdir(self.input_path):
            raise Exception('Input path "{input_path}" is not a folder'.format(input_path=self.input_path))

        if not os.path.isdir(self.output_path):
            os.makedirs(self.output_path)

    def unzip(self):
        files_in_input_path = os.listdir(self.input_path)
        files_to_unzip = [file_name for file_name in files_in_input_path if file_name.endswith(self.ZIP_EXTENSION)]

        number_of_zipped_files = len(files_to_unzip)
        print 'Found {number_of_zipped_files} zipped files.'.format(number_of_zipped_files=number_of_zipped_files)
        few_files = number_of_zipped_files <= 100

        for zip_file_index, zip_file_name in enumerate(files_to_unzip):
            input_file_path = os.path.join(self.input_path, zip_file_name)

            pdb_file_name = zip_file_name.replace(self.ZIP_EXTENSION, self.PDB_EXTENSION)
            output_file_path = os.path.join(self.output_path, pdb_file_name)

            with gzip.open(input_file_path, 'r') as zipped_file:
                with open(output_file_path, 'w') as pdb_file:
                    pdb_file.writelines(zipped_file.readlines())

            if few_files or zip_file_index % 100 == 0:
                print '\t{progress}%'.format(progress=zip_file_index * 100.0 / number_of_zipped_files)
