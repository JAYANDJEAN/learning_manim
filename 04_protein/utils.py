from typing import Union

import numpy as np
from Bio import PDB


class Element:
    def __repr__(self) -> str:
        return f"Element {self.atomic_number}: {self.name} ({self.symbol})"

    def __init__(self, element_ref: Union[str, int] = None):
        ELEMENT_DICT_ENG = {
            'H': ("H", "Hydrogen", 1, 1.007, "#ffffff"),
            'He': ("He", "Helium", 2, 4.002, "#d9ffff"),
            'Li': ("Li", "Lithium", 3, 6.941, "#cc80ff"),
            'Be': ("Be", "Beryllium", 4, 9.012, "#c2ff00"),
            'B': ("B", "Boron", 5, 10.811, "#ffb5b5"),
            'C': ("C", "Carbon", 6, 12.011, "#909090"),
            'N': ("N", "Nitrogen", 7, 14.007, "#3050f8"),
            'O': ("O", "Oxygen", 8, 15.999, "#ff0d0d"),
            'F': ("F", "Fluorine", 9, 18.998, "#90e050"),
            'Ne': ("Ne", "Neon", 10, 20.18, "#b3e3f5"),
            'Na': ("Na", "Sodium", 11, 22.99, "#ab5cf2"),
            'Mg': ("Mg", "Magnesium", 12, 24.305, "#8aff00"),
            'Al': ("Al", "Aluminum", 13, 26.982, "#bfa6a6"),
            'Si': ("Si", "Silicon", 14, 28.086, "#f0c8a0"),
            'P': ("P", "Phosphorus", 15, 30.974, "#ff8000"),
            'S': ("S", "Sulfur", 16, 32.065, "#ffff30"),
            'Cl': ("Cl", "Chlorine", 17, 35.453, "#1ff01f"),
            'Ar': ("Ar", "Argon", 18, 39.948, "#80d1e3"),
            'K': ("K", "Potassium", 19, 39.098, "#8f40d4"),
            'Ca': ("Ca", "Caclium", 20, 40.078, "#3dff00"),
            'Sc': ("Sc", "Scandium", 21, 44.956, "#e6e6e6"),
            'Ti': ("Ti", "Titanium", 22, 47.867, "#bfc2c7"),
            'V': ("V", "Vanadium", 23, 50.942, "#a6a6ab"),
            'Cr': ("Cr", "Chromium", 24, 51.996, "#8a99c7"),
            'Mn': ("Mn", "Manganese", 25, 54.938, "#9c7ac7"),
            'Fe': ("Fe", "Iron", 26, 55.845, "#e06633"),
            'Co': ("Co", "Cobalt", 27, 58.933, "#f090a0"),
            'Ni': ("Ni", "Nickel", 28, 58.693, "#50d050"),
            'Cu': ("Cu", "Copper", 29, 63.546, "#c88033"),
            'Zn': ("Zn", "Zinc", 30, 65.38, "#7d80b0"),
            'Ga': ("Ga", "Gallium", 31, 69.723, "#c28f8f"),
            'Ge': ("Ge", "Germanium", 32, 72.64, "#668f8f"),
            'As': ("As", "Arsenic", 33, 74.922, "#bd80e3"),
            'Se': ("Se", "Selenium", 34, 78.96, "#ffa100"),
            'Br': ("Br", "Bromine", 35, 79.904, "#a62929"),
            'Kr': ("Kr", "Krypton", 36, 83.798, "#5cb8d1"),
            'Rb': ("Rb", "Rubidium", 37, 85.468, "#702eb0"),
            'Sr': ("Sr", "Strontium", 38, 87.62, "#00ff00"),
            'Y': ("Y", "Yttrium", 39, 88.906, "#94ffff"),
            'Zr': ("Zr", "Zirconium", 40, 91.224, "#94e0e0"),
            'Nb': ("Nb", "Niobium", 41, 92.906, "#73c2c9"),
            'Mo': ("Mo", "Molybdenum", 42, 95.96, "#54b5b5"),
            'Tc': ("Tc", "Technitium", 43, 98.0, "#3b9e9e"),
            'Ru': ("Ru", "Ruthenium", 44, 101.07, "#248f8f"),
            'Rh': ("Rh", "Rhodium", 45, 102.906, "#0a7d8c"),
            'Pd': ("Pd", "Palladium", 46, 106.42, "#006985"),
            'Ag': ("Ag", "Silver", 47, 107.868, "#c0c0c0"),
            'Cd': ("Cd", "Cadmium", 48, 112.411, "#ffd98f"),
            'In': ("In", "Indium", 49, 114.818, "#a67573"),
            'Sn': ("Sn", "Tin", 50, 118.71, "#668080"),
            'Sb': ("Sb", "Antimony", 51, 121.76, "#9e63b5"),
            'Te': ("Te", "Tellerium", 52, 127.6, "#d47a00"),
            'I': ("I", "Iodine", 53, 126.904, "#940094"),
            'Xe': ("Xe", "Xeon", 54, 131.293, "#429eb0"),
            'Cs': ("Cs", "Cesium", 55, 132.905, "#57178f"),
            'Ba': ("Ba", "Barium", 56, 137.327, "#00c900"),
            'La': ("La", "Lanthanum", 57, 138.905, "#70d4ff"),
            'Ce': ("Ce", "Cerium", 58, 140.116, "#ffffc7"),
            'Pr': ("Pr", "Praseodymium", 59, 140.908, "#d9ffc7"),
            'Nd': ("Nd", "Neodymium", 60, 144.242, "#c7ffc7"),
            'Pm': ("Pm", "Promethium", 61, 145.0, "#a3ffc7"),
            'Sm': ("Sm", "Samarium", 62, 150.36, "#8fffc7"),
            'Eu': ("Eu", "Europium", 63, 151.964, "#61ffc7"),
            'Gd': ("Gd", "Gadolinium", 64, 157.25, "#45ffc7"),
            'Tb': ("Tb", "Terbium", 65, 158.925, "#30ffc7"),
            'Dy': ("Dy", "Dysprosium", 66, 162.5, "#1fffc7"),
            'Ho': ("Ho", "Holmium", 67, 164.93, "#00ff9c"),
            'Er': ("Er", "Erbium", 68, 167.259, "#00e675"),
            'Tm': ("Tm", "Thulium", 69, 168.934, "#00d452"),
            'Yb': ("Yb", "Ytterbium", 70, 173.054, "#00bf38"),
            'Lu': ("Lu", "Lutetium", 71, 174.967, "#00ab24"),
            'Hf': ("Hf", "Hafnium", 72, 178.49, "#4dc2ff"),
            'Ta': ("Ta", "Tantalum", 73, 180.948, "#4da6ff"),
            'W': ("W", "Tungsten", 74, 183.84, "#2194d6"),
            'Re': ("Re", "Rhenium", 75, 186.207, "#267dab"),
            'Os': ("Os", "Osmium", 76, 190.23, "#266696"),
            'Ir': ("Ir", "Iridium", 77, 192.217, "#175487"),
            'Pt': ("Pt", "Platinum", 78, 195.084, "#d0d0e0"),
            'Au': ("Au", "Gold", 79, 196.967, "#ffd123"),
            'Hg': ("Hg", "Mercury", 80, 200.59, "#b8b8d0"),
            'Tl': ("Tl", "Thallium", 81, 204.383, "#a6544d"),
            'Pb': ("Pb", "Lead", 82, 207.2, "#575961"),
            'Bi': ("Bi", "Bismuth", 83, 208.98, "#9e4fb5"),
            'Po': ("Po", "Polonium", 84, 210.0, "#ab5c00"),
            'At': ("At", "Astatine", 85, 210.0, "#754f45"),
            'Rn': ("Rn", "Radon", 86, 222.0, "#428296"),
            'Fr': ("Fr", "Francium", 87, 223.0, "#420066"),
            'Ra': ("Ra", "Radium", 88, 226.0, "#007d00"),
            'Ac': ("Ac", "Actinium", 89, 227.0, "#70abfa"),
            'Th': ("Th", "Thorium", 90, 232.038, "#00baff"),
            'Pa': ("Pa", "Protactinium", 91, 231.036, "#00a1ff"),
            'U': ("U", "Uranium", 92, 238.029, "#008fff"),
            'Np': ("Np", "Neptunium", 93, 237.0, "#0080ff"),
            'Pu': ("Pu", "Plutonium", 94, 244.0, "#006bff"),
            'Am': ("Am", "Americium", 95, 243.0, "#545cf2"),
            'Cm': ("Cm", "Curium", 96, 247.0, "#785ce3"),
            'Bk': ("Bk", "Berkelium", 97, 247.0, "#8a4fe3"),
            'Cf': ("Cf", "Californium", 98, 251.0, "#a136d4"),
            'Es': ("Es", "Einsteinium", 99, 252.0, "#b31fd4"),
            'Fm': ("Fm", "Fermium", 100, 257.0, "#b31fba"),
            'Md': ("Md", "Mendelevium", 101, 258.0, "#b30da6"),
            'No': ("No", "Nobelium", 102, 259.0, "#bd0d87"),
            'Lr': ("Lr", "Lawrencium", 103, 262.0, "#c70066"),
            'Rf': ("Rf", "Rutherfordium", 104, 261.0, "#cc0059"),
            'Db': ("Db", "Dubnium", 105, 262.0, "#d1004f"),
            'Sg': ("Sg", "Seaborgium", 106, 266.0, "#d90045"),
            'Bh': ("Bh", "Bohrium", 107, 264.0, "#e00038"),
            'Hs': ("Hs", "Hassium", 108, 267.0, "#e6002e"),
            'Mt': ("Mt", "Meitnerium", 109, 268.0, "#eb0026"),
            'Ds': ("Ds", "Darmstadtium", 110, 271.0, "#eb0026"),
            'Rg': ("Rg", "Roentgenium", 111, 272.0, "#eb0026"),
            'Cn': ("Cn", "Copernicium", 112, 285.0, "#eb0026"),
            'Nh': ("Nh", "Nihonium", 113, 284.0, "#eb0026"),
            'Fl': ("Fl", "Flerovium", 114, 289.0, "#eb0026"),
            'Mc': ("Mc", "Moscovium", 115, 288.0, "#eb0026"),
            'Lv': ("Lv", "Livermorium", 116, 292.0, "#eb0026"),
            'Ts': ("Ts", "Tennessine", 117, 295.0, "#eb0026"),
            'Og': ("Og", "Oganesson", 118, 294.0, "#eb0026"),
        }
        if isinstance(element_ref, str):
            element = ELEMENT_DICT_ENG.get(element_ref, 'H')
        elif isinstance(element_ref, int):
            keys = list(ELEMENT_DICT_ENG.keys())
            key = keys[element_ref - 1] if element_ref <= len(keys) else 'H'
            element = ELEMENT_DICT_ENG[key]
        else:
            element = ELEMENT_DICT_ENG['H']
        self.symbol = element[0]
        self.name = element[1]
        self.atomic_number = element[2]
        self.mass = element[3]
        self.color = element[4]


def mol_parser(file):
    with open(file) as file:
        mol_file = file.readlines()
    mol_general_info = mol_file[3]
    mol_file.remove(mol_general_info)
    mol_general_info = mol_general_info.rstrip().split()
    number_of_atoms = int(mol_general_info[0])
    number_of_bonds = int(mol_general_info[1])

    atoms = {}
    bonds = {}
    for index, line in enumerate(mol_file[3: 3 + number_of_atoms]):
        line_data = line.split()
        x_position = float(line_data[0])
        y_position = float(line_data[1])
        z_position = float(line_data[2])
        element = line_data[3]
        atoms[index + 1] = {
            "cords": np.array([x_position, y_position, z_position]),
            "element": element,
        }

    for line in mol_file[3 + number_of_atoms: 3 + number_of_atoms + number_of_bonds]:
        line_data = line.split()
        first_atom_index = int(float(line_data[0]))
        second_atom_index = int(float(line_data[1]))
        bond_type = line_data[2]
        bond_data = {
            "to": second_atom_index,
            "type": bond_type,
        }

        if first_atom_index not in bonds:
            bonds[first_atom_index] = [bond_data]
            if not atoms.get(first_atom_index) or not atoms.get(first_atom_index).get(
                    "bond_to"
            ):
                atoms[first_atom_index]["bond_to"] = {
                    second_atom_index: atoms.get(second_atom_index).get("element")
                }
            else:
                atoms[first_atom_index]["bond_to"][second_atom_index] = atoms.get(
                    second_atom_index
                ).get("element")
        else:
            bonds[first_atom_index].append(bond_data)
            atoms[first_atom_index]["bond_to"][second_atom_index] = atoms.get(
                second_atom_index
            ).get("element")

    return atoms, bonds


def pdb_parser(file):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure('pdb', file)
    atoms = {}
    bonds = {}
    index = 0
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    cords = atom.coord
                    atoms[index + 1] = {
                        "cords": np.array([cords[0], cords[1], cords[2]]),
                        "element": atom.element,
                    }
                    index += 1

    return atoms, bonds


if __name__ == "__main__":
    data1 = mol_parser('data/morphine3d.mol')
    print(data1[0])
    print(data1[1])
