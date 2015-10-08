import argparse
import sys

from edirp.file_downloader import FileDownloader
from edirp.unzipper import Unzipper
from edirp.filter_converter import FilterConverter


class EdirpParser:
    PULL = 'pull'
    UNZIP = 'unzip'
    CONVERT = 'convert'

    def __init__(self):
        self.parser = argparse.ArgumentParser()

        subparsers = self.parser.add_subparsers(
            dest='subcommand',
            title='subparsers',
            description='valid subcommands',
            help='choose one!'
        )

        self.pull_parser = subparsers.add_parser(self.PULL)
        self.pull_parser.add_argument('--working-dir', help='BS. TBD')
        self.pull_parser.add_argument('--max-number', type=int, help='If you don\'t want to download al the 10K+ '
                                                                     'structures for testing, chose this')

        self.unzip_parser = subparsers.add_parser(self.UNZIP)
        self.unzip_parser.add_argument('--working-dir', help='BS. TBD')

        self.convert_parser = subparsers.add_parser(self.CONVERT)
        self.convert_parser.add_argument('--working-dir', help='BS. TBD')
        self.convert_parser.add_argument('--min-resolution', type=float, help='All the structures with lower '
                                                                              'resolution will be discarded.')
        self.convert_parser.add_argument('--min-chain-length', type=int, help='All the chains shorter than this will '
                                                                              'be discarded.')

if __name__ == '__main__':
    edirp_parser = EdirpParser()
    namespace = edirp_parser.parser.parse_args(sys.argv[1:])

    if namespace.subcommand == EdirpParser.PULL:
        FileDownloader(working_directory=namespace.working_dir, max_number=namespace.max_number).pull()

    if namespace.subcommand == EdirpParser.UNZIP:
        Unzipper(working_dir=namespace.working_dir).unzip()

    if namespace.subcommand == EdirpParser.CONVERT:

        FilterConverter(**vars(namespace)).filter_and_convert()
