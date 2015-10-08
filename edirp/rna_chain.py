import os
import json


class RNAChain:
    CHAIN_ID_COLUMN = 21
    RESIDUE_ID_COLUMNS = slice(22, 26)
    RESIDUE_COLUMN = 19
    RNA_RESIDUES = 'AUGC'
    X_COORD_COLUMNS = slice(31, 39)
    Y_COORD_COLUMNS = slice(39, 47)
    Z_COORD_COLUMNS = slice(47, 55)

    def __init__(self, chain_id, atoms):
        self.chain_id = chain_id
        self.atoms = atoms

    def is_RNA(self):
        return all([atom_line[self.RESIDUE_COLUMN] in self.RNA_RESIDUES for atom_line in self.atoms])

    def get_length(self):
        return len(self.atoms)

    def write_to_file(self, path, pdb_object):
        file_name = '{pdb_id}_{chain_id}.json'.format(pdb_id=pdb_object.pdb_id, chain_id=self.chain_id)

        with open(os.path.join(path, file_name), 'w') as output_file:
            atom_coords = []

            for atom_line in self.atoms:
                atom_coords.append({
                    'x': float(atom_line[self.X_COORD_COLUMNS]),
                    'y': float(atom_line[self.Y_COORD_COLUMNS]),
                    'z': float(atom_line[self.Z_COORD_COLUMNS]),
                })

            dump_object = {
                'meta': {
                    'pdb_id': pdb_object.pdb_id,
                    'chain_id': self.chain_id,
                    'resolution': pdb_object.resolution,
                },
                'atom_coords': atom_coords,
            }

            json.dump(dump_object, output_file)

    @classmethod
    def get_chains_from_atoms(cls, atoms, min_length):
        atoms_by_chain = cls._get_atoms_by_chain(atoms)
        chains = [RNAChain(chain_id, chain_atoms) for (chain_id, chain_atoms) in atoms_by_chain.iteritems()]
        return [chain for chain in chains if chain.is_RNA() and chain.get_length() > min_length]

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
    def _distinct_atoms(cls, atom_list):
        distinct_atoms = []
        residue_ids = set()

        for atom_line in atom_list:

            residue_id = atom_line[cls.RESIDUE_ID_COLUMNS]
            if residue_id not in residue_ids:
                distinct_atoms.append(atom_line)
                residue_ids.add(residue_id)

        return distinct_atoms
