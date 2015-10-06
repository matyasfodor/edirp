import argparse
import sys

from edirp.file_downloader import FileDownloader


class EdirpParser:
    PULL = 'pull'

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
        pull_parser.add_argument('--target', help='destination path to download the PDB files. '
                                                  'If no destination provided, a temporary directory '
                                                  'will be used.')

        return parser


if __name__ == '__main__':
    edirp_parser = EdirpParser()
    namespace = edirp_parser.parser.parse_args(sys.argv[1:])

    if namespace.subcommand == EdirpParser.PULL:
        file_downloader = FileDownloader(target_folder=namespace.target)
        file_downloader.pull()
