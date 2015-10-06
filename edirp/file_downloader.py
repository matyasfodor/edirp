import ftplib
import tempfile
import os


class FileDownloader:
    HOSTNAME = "ftp.wwpdb.org"
    FTP_PATH = "/pub/pdb/data/structures/all/pdb/"
    # PREFIX = "pdb"
    # SUFFIX = ".ent.gz"

    def __init__(self, target_folder=None, host_name=HOSTNAME, ftp_path=FTP_PATH):
        self.ftp_connection = None
        self.host_name = host_name
        self.ftp_path = ftp_path
        self.target_folder = target_folder

        if self.target_folder is None:
            tempdir = tempfile.mkdtemp()
            print 'No target directory found, "{tempdir}" will be used to store the pdb files.'.format(tempdir=tempdir)
            self.target_folder = tempdir

        if not os.path.isdir(self.target_folder):
            os.makedirs(self.target_folder)

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

        filenames_in_dir = self.ftp_connection.nlst()
        pdb_files = [filename for filename in filenames_in_dir if filename.startswith('pdb')]

        number_of_pdb_files = len(pdb_files)
        print 'found {number_of_pdb_files} pdb files.'.format(number_of_pdb_files=number_of_pdb_files)
        few_files = number_of_pdb_files < 100

        for pdb_file_index, pdb_file in enumerate(pdb_files):

            output_path = os.path.join(self.target_folder, pdb_file)
            with open(output_path, 'wb') as output_file:
                self.ftp_connection.retrbinary('RETR {filename}'.format(filename=pdb_file), output_file.write)

            if few_files or pdb_file_index % 100 == 0:
                print '{progress}%'.format(progress=pdb_file_index * 100.0 / number_of_pdb_files)

        self.quit_connection()
