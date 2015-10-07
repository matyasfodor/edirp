import argparse
import sys

from edirp.file_downloader import FileDownloader
from edirp.unzipper import Unzipper


class EdirpParser:
    PULL = 'pull'
    UNZIP = 'unzip'

    def __init__(self):
        self.parser = self.get_parser()

    @classmethod
    def get_parser(cls):
        parser = argparse.ArgumentParser()

        subparsers = parser.add_subparsers(
            dest='subcommand',
            title='subparsers',
            description='valid subcommands',
            help='choose one!'
        )

        pull_parser = subparsers.add_parser(cls.PULL)
        pull_parser.add_argument('--working_dir', help='destination path to download the PDB files. '
                                                       'If no destination provided, a temporary directory '
                                                       'will be used.')
        pull_parser.add_argument('--max_number', type=int, help='If you don\'t want to download al the 10K+ structures '
                                                                'for testing, chose this')

        unzip_parser = subparsers.add_parser(cls.UNZIP)
        unzip_parser.add_argument('--working_dir', help='destination path to download the PDB files. '
                                                        'If no destination provided, a temporary directory '
                                                        'will be used.')

        return parser


if __name__ == '__main__':
    edirp_parser = EdirpParser()
    namespace = edirp_parser.parser.parse_args(sys.argv[1:])

    if namespace.subcommand == EdirpParser.PULL:
        file_downloader = FileDownloader(working_directory=namespace.working_dir, max_number=namespace.max_number)
        file_downloader.pull()

    if namespace.subcommand == EdirpParser.UNZIP:
        unzipper = Unzipper(working_dir=namespace.working_dir)
        unzipper.unzip()