import numpy as np
from pymol import cmd
from rdkit import Chem


def add_h():
    cmd.load("data/A0A4W3JAN5_min.pdb")
    cmd.h_add()
    cmd.save("data/A0A4W3JAN5_min.mol", format="mol")


def parser_mol():
    mol = Chem.MolFromMolFile('data/morphine3d.mol')
    mol_with_h = Chem.AddHs(mol)
    conformer = mol_with_h.GetConformer()
    atoms = {}
    bonds = {}
    for atom in mol_with_h.GetAtoms():
        atom_idx = atom.GetIdx()
        pos = conformer.GetAtomPosition(atom_idx)
        atoms[atom_idx + 1] = {
            "cords": np.array(pos),
            "element": atom.GetSymbol(),
        }
    # 因为 AROMATIC 无法区分单键还是双键，所以不考虑用rdkit解析mol文件
    for bond in mol_with_h.GetBonds():
        print(f"Bond between atom {bond.GetBeginAtomIdx()} and {bond.GetEndAtomIdx()}, {bond.GetBondTypeAsDouble()}")


parser_mol()
