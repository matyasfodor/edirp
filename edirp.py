import argparse
import sys

from edirp.edirp_config_parser import EdirpConfigParser
from edirp.file_downloader import FileDownloader
from edirp.unzipper import Unzipper
from edirp.filter_converter import FilterConverter


class EdirpParser:
    CONFIG = 'config'
    PULL = 'pull'
    UNZIP = 'unzip'
    CONVERT_JSON = 'convert-json'
    CONVERT_EDIRP = 'convert-edirp'

    def __init__(self):
        self.parser = argparse.ArgumentParser()

        subparsers = self.parser.add_subparsers(
            dest='subcommand',
            title='subparsers',
            description='valid subcommands',
            help='choose one!'
        )

        self.parser.add_argument('--config-file', help='Path to the json config file')

        subparsers.add_parser(self.CONFIG)

        self.pull_parser = subparsers.add_parser(self.PULL)
        self.pull_parser.add_argument('--working-dir', help='BS. TBD')
        self.pull_parser.add_argument('--max-number', type=int, help='If you don\'t want to download al the 10K+ '
                                                                     'structures for testing, chose this')

        self.unzip_parser = subparsers.add_parser(self.UNZIP)
        self.unzip_parser.add_argument('--working-dir', help='BS. TBD')

        self.convert_json_parser = subparsers.add_parser(self.CONVERT_JSON)
        self.convert_json_parser.add_argument('--working-dir', help='BS. TBD')
        self.convert_json_parser.add_argument('--min-resolution', type=float, help='All the structures with lower '
                                                                              'resolution will be discarded.')
        self.convert_json_parser.add_argument('--min-chain-length', type=int, help='All the chains shorter than this will '
                                                                              'be discarded.')

        self.convert_edirp_parser = subparsers.add_parser(self.CONVERT_EDIRP)
        self.convert_edirp_parser.add_argument('--working-dir', help='BS. TBD')
        self.convert_edirp_parser.add_argument('--config-json', help='the conversion configuration file. '
                                                                    'TODO: add interactive cofniguration tool')

if __name__ == '__main__':
    edirp_parser = EdirpParser()
    namespace = edirp_parser.parser.parse_args(sys.argv[1:])

    if namespace.subcommand == EdirpParser.CONFIG:
        EdirpConfigParser.create_config_interactively()

    if namespace.subcommand == EdirpParser.PULL:
        FileDownloader(**vars(namespace)).pull()

    if namespace.subcommand == EdirpParser.UNZIP:
        Unzipper(working_dir=namespace.working_dir).unzip()

    if namespace.subcommand == EdirpParser.CONVERT_JSON:

        FilterConverter(**vars(namespace)).filter_and_convert_to_json()

    if namespace.subcommand == EdirpParser.CONVERT_EDIRP:

        FilterConverter(**vars(namespace)).filter_and_convert_to_edirp()
