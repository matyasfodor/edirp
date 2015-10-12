import ftplib
import tempfile
import os

from .edirp_config_parser import EdirpConfigParser


class FileDownloader:
    HOSTNAME = "ftp.wwpdb.org"
    FTP_PATH = "/pub/pdb/data/structures/all/pdb/"
    TARGET_FOLDER = 'downloaded'
    # PREFIX = "pdb"
    # SUFFIX = ".ent.gz"

    def __init__(self, **kwargs):
        config = EdirpConfigParser(**kwargs).get_config()

        self.ftp_connection = None
        self.host_name = config.get('host_name') or self.HOSTNAME
        self.ftp_path = config.get('ftp_path') or self.FTP_PATH

        self.max_number = config.get('max_number')

        working_dir = config['working_dir']

        self.target_path = os.path.join(working_dir, self.TARGET_FOLDER)

        if not os.path.isdir(self.target_path):
            os.makedirs(self.target_path)

    def connect_ftp(self):
        if self.ftp_connection is None:
            self.ftp_connection = ftplib.FTP()
            self.ftp_connection.connect(self.host_name)
            self.ftp_connection.login()

    def quit_connection(self):
        self.ftp_connection.quit()

    def pull(self):
        self.connect_ftp()
        self.ftp_connection.cwd(self.ftp_path)

        print 'Downloading file list..'
        filenames_in_dir = self.ftp_connection.nlst()
        files = [filename for filename in filenames_in_dir if filename.startswith('pdb')]

        if self.max_number is not None:
            files = files[:self.max_number]

        number_of_files = len(files)
        print 'Found {number_of_files} pdb files.'.format(number_of_files=number_of_files)
        few_files = number_of_files <= 100

        for file_name_index, file_name in enumerate(files):

            output_path = os.path.join(self.target_path, file_name)
            with open(output_path, 'wb') as output_file:
                self.ftp_connection.retrbinary('RETR {file_name}'.format(file_name=file_name), output_file.write)

            if few_files or file_name_index % 100 == 0:
                print '\t{progress}%'.format(progress=file_name_index * 100.0 / number_of_files)

        self.quit_connection()
