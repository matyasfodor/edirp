import gzip

from rna_chain import RNAChain


class PDBFile:
    RESOLUTION_COLUMN = 3
    HEADER_COLUMNS = slice(62, 66)

    REMARK = 'REMARK'
    RESOLUTION_REMARK_NUMBER = '2'
    RESOLUTION = 'RESOLUTION.'
    RESOLUTION_LINE_MATCHER = [REMARK, RESOLUTION_REMARK_NUMBER, RESOLUTION]

    ATOM = 'ATOM'
    ATOM_LINE_MATCHER = [ATOM, None]

    HEADER = 'HEADER'
    HEADER_MATCHER = [HEADER]

    def __init__(self, file_lines, filtered_atom_type):
        self.lines = file_lines
        self.pdb_id = self._get_pdb_id()
        self.resolution = self._get_resolution()
        self.atom_line_matcher = self.ATOM_LINE_MATCHER + [filtered_atom_type]
        self.atoms = self._get_atoms()

    def _get_pdb_id(self):
        for line in self.lines:
            line_array = line.split()
            if self.line_matcher(line_array, self.HEADER_MATCHER):
                return line[self.HEADER_COLUMNS]
        raise Exception('PDB id not found.')

    def _get_resolution(self):
        for line in self.lines:
            line_array = line.split()
            if self.line_matcher(line_array, self.RESOLUTION_LINE_MATCHER):
                try:
                    return float(line_array[self.RESOLUTION_COLUMN].strip())
                except ValueError:
                    return None

        return None

    def _get_atoms(self):
        return [line for line in self.lines if self.line_matcher(line.split(), self.atom_line_matcher)]

    @staticmethod
    def line_matcher(line_array, expected):

        if len(expected) > len(line_array):
            return False

        for (expected_element, line_element) in zip(expected, line_array):
            if expected_element is not None and expected_element != line_element:
                return False

        return True

    @classmethod
    def from_zip(cls, file_name, filtered_atom_type):
        zipped_file = gzip.open(file_name, 'r')
        return PDBFile(zipped_file.readlines(), filtered_atom_type)

    def has_better_resolution(self, required_resolution):
        return self.resolution and self.resolution < required_resolution

    def get_chains(self, min_length):
        return RNAChain.get_chains_from_atoms(self, min_length)
