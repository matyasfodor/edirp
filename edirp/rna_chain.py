import os
import json
import numpy


class RNAChain:
    CHAIN_ID_COLUMN = 21
    RESIDUE_ID_COLUMNS = slice(22, 26)
    RESIDUE_COLUMN = 19
    RNA_RESIDUES = 'AUGC'
    X_COORD_COLUMNS = slice(31, 39)
    Y_COORD_COLUMNS = slice(39, 47)
    Z_COORD_COLUMNS = slice(47, 55)

    def __init__(self, chain_id, pdb_object, atoms, config):
        self.config = config

        self.chain_id = chain_id
        self.pdb_id = pdb_object.pdb_id
        self.resolution = pdb_object.resolution
        self.atoms = atoms

    def is_rna(self):
        return all([atom['residue'] in self.RNA_RESIDUES for atom in self.atoms])

    def get_length(self):
        return len(self.atoms)

    def write_to_file(self, path):
        file_name = '{pdb_id}_{chain_id}.json'.format(pdb_id=self.pdb_id, chain_id=self.chain_id)

        with open(os.path.join(path, file_name), 'w') as output_file:
            dump_object = {
                'meta': {
                    'pdb_id': self.pdb_id,
                    'chain_id': self.chain_id,
                    'resolution': self.resolution,
                },
                'atoms': self.atoms,
            }

            json.dump(dump_object, output_file)

    def write_to_edirp_file(self, path):
        file_name = '{pdb_id}_{chain_id}.pdb.json'.format(pdb_id=self.pdb_id, chain_id=self.chain_id)
        distribution = self._get_distribution()

        with open(os.path.join(path, file_name), 'w') as output_file:
            dump_object = {
                'meta': {
                    'pdb_id': self.pdb_id,
                    'chain_id': self.chain_id,
                    'resolution': self.resolution,
                    'edirp_level_ranges_name': self.config['edirp_level_ranges'].name
                },
                'distribution': distribution,
            }

            json.dump(dump_object, output_file)

    @classmethod
    def get_chains_from_atoms(cls, pdb_object, min_length, config):
        atoms = pdb_object.atoms

        atoms_lines_by_chain = cls._get_atoms_by_chain(atoms)

        atom_objects_by_chain = {key: cls._get_atom_coords_from_line(value) for
                                 key, value in atoms_lines_by_chain.items()}

        chains = [RNAChain(chain_id, pdb_object, chain_atoms, config) for
                  (chain_id, chain_atoms) in atom_objects_by_chain.iteritems()]

        return [chain for chain in chains if chain.is_rna() and chain.get_length() > min_length]

    @classmethod
    def _get_atoms_by_chain(cls, atoms):
        atoms_by_chain = {}

        for atom_line in atoms:
            chain_id = atom_line[cls.CHAIN_ID_COLUMN]
            atoms_by_chain.setdefault(chain_id, []).append(atom_line)

        distinct_atoms_by_chain = {}

        for (chain_id, atom_list) in atoms_by_chain.iteritems():
            distinct_atoms_by_chain[chain_id] = cls._distinct_atoms(atom_list)

        return distinct_atoms_by_chain

    @classmethod
    def _get_atom_coords_from_line(cls, atom_lines):
        atoms = []
        for atom_line in atom_lines:
            atoms.append({
                'coordinates': {
                    'x': float(atom_line[cls.X_COORD_COLUMNS]),
                    'y': float(atom_line[cls.Y_COORD_COLUMNS]),
                    'z': float(atom_line[cls.Z_COORD_COLUMNS]),
                },
                'residue': atom_line[cls.RESIDUE_COLUMN],
            })

        return atoms

    # TODO filter based on occupancy
    @classmethod
    def _distinct_atoms(cls, atom_list):
        distinct_atoms = []
        residue_ids = set()

        for atom_line in atom_list:

            residue_id = atom_line[cls.RESIDUE_ID_COLUMNS]
            if residue_id not in residue_ids:
                distinct_atoms.append(atom_line)
                residue_ids.add(residue_id)

        return distinct_atoms

    def _get_distribution(self):
        distances = []
        for index, first_atom in enumerate(self.atoms):
            for second_atom in self.atoms[index+1:]:
                distances.append(self._compute_atom_distance(first_atom['coordinates'], second_atom['coordinates']))
        return self.config['edirp_level_ranges'].create_histogram(distances)

    @staticmethod
    def _compute_atom_distance(first_atom, second_atom):
        first_atom_coord = numpy.array((first_atom['x'], first_atom['y'], first_atom['z'],))
        second_atom_coord = numpy.array((second_atom['x'], second_atom['y'], second_atom['z'],))

        return numpy.linalg.norm(first_atom_coord-second_atom_coord)
