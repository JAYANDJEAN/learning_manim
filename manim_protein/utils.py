from dataclasses import dataclass

import numpy as np
import pandas as pd
from manim import ORIGIN, TAU, PI
from manim.mobject.opengl.opengl_surface import OpenGLSurface


@dataclass
class GenericElement:
    symbol: str
    name: str
    atomic_number: int
    mass: float
    cpk_color: str


ELEMENT_DICT_ENG = {
    'H ': GenericElement("H", "Hydrogen", 1, 1.007, "#ffffff"),
    'He ': GenericElement("He", "Helium", 2, 4.002, "#d9ffff"),
    'Li ': GenericElement("Li", "Lithium", 3, 6.941, "#cc80ff"),
    'Be ': GenericElement("Be", "Beryllium", 4, 9.012, "#c2ff00"),
    'B ': GenericElement("B", "Boron", 5, 10.811, "#ffb5b5"),
    'C ': GenericElement("C", "Carbon", 6, 12.011, "#909090"),
    'N ': GenericElement("N", "Nitrogen", 7, 14.007, "#3050f8"),
    'O ': GenericElement("O", "Oxygen", 8, 15.999, "#ff0d0d"),
    'F ': GenericElement("F", "Fluorine", 9, 18.998, "#90e050"),
    'Ne ': GenericElement("Ne", "Neon", 10, 20.18, "#b3e3f5"),
    'Na ': GenericElement("Na", "Sodium", 11, 22.99, "#ab5cf2"),
    'Mg ': GenericElement("Mg", "Magnesium", 12, 24.305, "#8aff00"),
    'Al ': GenericElement("Al", "Aluminum", 13, 26.982, "#bfa6a6"),
    'Si ': GenericElement("Si", "Silicon", 14, 28.086, "#f0c8a0"),
    'P ': GenericElement("P", "Phosphorus", 15, 30.974, "#ff8000"),
    'S ': GenericElement("S", "Sulfur", 16, 32.065, "#ffff30"),
    'Cl ': GenericElement("Cl", "Chlorine", 17, 35.453, "#1ff01f"),
    'Ar ': GenericElement("Ar", "Argon", 18, 39.948, "#80d1e3"),
    'K ': GenericElement("K", "Potassium", 19, 39.098, "#8f40d4"),
    'Ca ': GenericElement("Ca", "Caclium", 20, 40.078, "#3dff00"),
    'Sc ': GenericElement("Sc", "Scandium", 21, 44.956, "#e6e6e6"),
    'Ti ': GenericElement("Ti", "Titanium", 22, 47.867, "#bfc2c7"),
    'V ': GenericElement("V", "Vanadium", 23, 50.942, "#a6a6ab"),
    'Cr ': GenericElement("Cr", "Chromium", 24, 51.996, "#8a99c7"),
    'Mn ': GenericElement("Mn", "Manganese", 25, 54.938, "#9c7ac7"),
    'Fe ': GenericElement("Fe", "Iron", 26, 55.845, "#e06633"),
    'Co ': GenericElement("Co", "Cobalt", 27, 58.933, "#f090a0"),
    'Ni ': GenericElement("Ni", "Nickel", 28, 58.693, "#50d050"),
    'Cu ': GenericElement("Cu", "Copper", 29, 63.546, "#c88033"),
    'Zn ': GenericElement("Zn", "Zinc", 30, 65.38, "#7d80b0"),
    'Ga ': GenericElement("Ga", "Gallium", 31, 69.723, "#c28f8f"),
    'Ge ': GenericElement("Ge", "Germanium", 32, 72.64, "#668f8f"),
    'As ': GenericElement("As", "Arsenic", 33, 74.922, "#bd80e3"),
    'Se ': GenericElement("Se", "Selenium", 34, 78.96, "#ffa100"),
    'Br ': GenericElement("Br", "Bromine", 35, 79.904, "#a62929"),
    'Kr ': GenericElement("Kr", "Krypton", 36, 83.798, "#5cb8d1"),
    'Rb ': GenericElement("Rb", "Rubidium", 37, 85.468, "#702eb0"),
    'Sr ': GenericElement("Sr", "Strontium", 38, 87.62, "#00ff00"),
    'Y ': GenericElement("Y", "Yttrium", 39, 88.906, "#94ffff"),
    'Zr ': GenericElement("Zr", "Zirconium", 40, 91.224, "#94e0e0"),
    'Nb ': GenericElement("Nb", "Niobium", 41, 92.906, "#73c2c9"),
    'Mo ': GenericElement("Mo", "Molybdenum", 42, 95.96, "#54b5b5"),
    'Tc ': GenericElement("Tc", "Technitium", 43, 98.0, "#3b9e9e"),
    'Ru ': GenericElement("Ru", "Ruthenium", 44, 101.07, "#248f8f"),
    'Rh ': GenericElement("Rh", "Rhodium", 45, 102.906, "#0a7d8c"),
    'Pd ': GenericElement("Pd", "Palladium", 46, 106.42, "#006985"),
    'Ag ': GenericElement("Ag", "Silver", 47, 107.868, "#c0c0c0"),
    'Cd ': GenericElement("Cd", "Cadmium", 48, 112.411, "#ffd98f"),
    'In ': GenericElement("In", "Indium", 49, 114.818, "#a67573"),
    'Sn ': GenericElement("Sn", "Tin", 50, 118.71, "#668080"),
    'Sb ': GenericElement("Sb", "Antimony", 51, 121.76, "#9e63b5"),
    'Te ': GenericElement("Te", "Tellerium", 52, 127.6, "#d47a00"),
    'I ': GenericElement("I", "Iodine", 53, 126.904, "#940094"),
    'Xe ': GenericElement("Xe", "Xeon", 54, 131.293, "#429eb0"),
    'Cs ': GenericElement("Cs", "Cesium", 55, 132.905, "#57178f"),
    'Ba ': GenericElement("Ba", "Barium", 56, 137.327, "#00c900"),
    'La ': GenericElement("La", "Lanthanum", 57, 138.905, "#70d4ff"),
    'Ce ': GenericElement("Ce", "Cerium", 58, 140.116, "#ffffc7"),
    'Pr ': GenericElement("Pr", "Praseodymium", 59, 140.908, "#d9ffc7"),
    'Nd ': GenericElement("Nd", "Neodymium", 60, 144.242, "#c7ffc7"),
    'Pm ': GenericElement("Pm", "Promethium", 61, 145.0, "#a3ffc7"),
    'Sm ': GenericElement("Sm", "Samarium", 62, 150.36, "#8fffc7"),
    'Eu ': GenericElement("Eu", "Europium", 63, 151.964, "#61ffc7"),
    'Gd ': GenericElement("Gd", "Gadolinium", 64, 157.25, "#45ffc7"),
    'Tb ': GenericElement("Tb", "Terbium", 65, 158.925, "#30ffc7"),
    'Dy ': GenericElement("Dy", "Dysprosium", 66, 162.5, "#1fffc7"),
    'Ho ': GenericElement("Ho", "Holmium", 67, 164.93, "#00ff9c"),
    'Er ': GenericElement("Er", "Erbium", 68, 167.259, "#00e675"),
    'Tm ': GenericElement("Tm", "Thulium", 69, 168.934, "#00d452"),
    'Yb ': GenericElement("Yb", "Ytterbium", 70, 173.054, "#00bf38"),
    'Lu ': GenericElement("Lu", "Lutetium", 71, 174.967, "#00ab24"),
    'Hf ': GenericElement("Hf", "Hafnium", 72, 178.49, "#4dc2ff"),
    'Ta ': GenericElement("Ta", "Tantalum", 73, 180.948, "#4da6ff"),
    'W ': GenericElement("W", "Tungsten", 74, 183.84, "#2194d6"),
    'Re ': GenericElement("Re", "Rhenium", 75, 186.207, "#267dab"),
    'Os ': GenericElement("Os", "Osmium", 76, 190.23, "#266696"),
    'Ir ': GenericElement("Ir", "Iridium", 77, 192.217, "#175487"),
    'Pt ': GenericElement("Pt", "Platinum", 78, 195.084, "#d0d0e0"),
    'Au ': GenericElement("Au", "Gold", 79, 196.967, "#ffd123"),
    'Hg ': GenericElement("Hg", "Mercury", 80, 200.59, "#b8b8d0"),
    'Tl ': GenericElement("Tl", "Thallium", 81, 204.383, "#a6544d"),
    'Pb ': GenericElement("Pb", "Lead", 82, 207.2, "#575961"),
    'Bi ': GenericElement("Bi", "Bismuth", 83, 208.98, "#9e4fb5"),
    'Po ': GenericElement("Po", "Polonium", 84, 210.0, "#ab5c00"),
    'At ': GenericElement("At", "Astatine", 85, 210.0, "#754f45"),
    'Rn ': GenericElement("Rn", "Radon", 86, 222.0, "#428296"),
    'Fr ': GenericElement("Fr", "Francium", 87, 223.0, "#420066"),
    'Ra ': GenericElement("Ra", "Radium", 88, 226.0, "#007d00"),
    'Ac ': GenericElement("Ac", "Actinium", 89, 227.0, "#70abfa"),
    'Th ': GenericElement("Th", "Thorium", 90, 232.038, "#00baff"),
    'Pa ': GenericElement("Pa", "Protactinium", 91, 231.036, "#00a1ff"),
    'U ': GenericElement("U", "Uranium", 92, 238.029, "#008fff"),
    'Np ': GenericElement("Np", "Neptunium", 93, 237.0, "#0080ff"),
    'Pu ': GenericElement("Pu", "Plutonium", 94, 244.0, "#006bff"),
    'Am ': GenericElement("Am", "Americium", 95, 243.0, "#545cf2"),
    'Cm ': GenericElement("Cm", "Curium", 96, 247.0, "#785ce3"),
    'Bk ': GenericElement("Bk", "Berkelium", 97, 247.0, "#8a4fe3"),
    'Cf ': GenericElement("Cf", "Californium", 98, 251.0, "#a136d4"),
    'Es ': GenericElement("Es", "Einsteinium", 99, 252.0, "#b31fd4"),
    'Fm ': GenericElement("Fm", "Fermium", 100, 257.0, "#b31fba"),
    'Md ': GenericElement("Md", "Mendelevium", 101, 258.0, "#b30da6"),
    'No ': GenericElement("No", "Nobelium", 102, 259.0, "#bd0d87"),
    'Lr ': GenericElement("Lr", "Lawrencium", 103, 262.0, "#c70066"),
    'Rf ': GenericElement("Rf", "Rutherfordium", 104, 261.0, "#cc0059"),
    'Db ': GenericElement("Db", "Dubnium", 105, 262.0, "#d1004f"),
    'Sg ': GenericElement("Sg", "Seaborgium", 106, 266.0, "#d90045"),
    'Bh ': GenericElement("Bh", "Bohrium", 107, 264.0, "#e00038"),
    'Hs ': GenericElement("Hs", "Hassium", 108, 267.0, "#e6002e"),
    'Mt ': GenericElement("Mt", "Meitnerium", 109, 268.0, "#eb0026"),
    'Ds ': GenericElement("Ds", "Darmstadtium", 110, 271.0, "#eb0026"),
    'Rg ': GenericElement("Rg", "Roentgenium", 111, 272.0, "#eb0026"),
    'Cn ': GenericElement("Cn", "Copernicium", 112, 285.0, "#eb0026"),
    'Nh ': GenericElement("Nh", "Nihonium", 113, 284.0, "#eb0026"),
    'Fl ': GenericElement("Fl", "Flerovium", 114, 289.0, "#eb0026"),
    'Mc ': GenericElement("Mc", "Moscovium", 115, 288.0, "#eb0026"),
    'Lv ': GenericElement("Lv", "Livermorium", 116, 292.0, "#eb0026"),
    'Ts ': GenericElement("Ts", "Tennessine", 117, 295.0, "#eb0026"),
    'Og ': GenericElement("Og", "Oganesson", 118, 294.0, "#eb0026"),
}


class Element:
    def __repr__(self) -> str:
        return f"Element {self.atomic_number}: {self.name} ({self.symbol})"

    def __init__(
            self,
            symbol: str = "H",
            name: str = "H",
            atomic_number: int = 1,
            mass: float = 1.008,
            color: str or None = "#FFFFFF",
    ):
        self.symbol = symbol
        self.name = name
        self.atomic_number = atomic_number
        self.mass = mass
        self.color = color or "#ff00ff"

    def from_csv_file(filename, element: str or int):
        use_valid_reference_string = f"What are you doing? Pass a valid atomic reference. {element} is NOT a valid reference"
        data = pd.read_csv(filename, index_col=False)

        if isinstance(element, str):
            search_column = "Symbol"

        elif isinstance(element, int) and element < 118:
            search_column = "AtomicNumber"

        else:
            raise Exception(use_valid_reference_string)

        subdata = data.loc[data[search_column] == element]

        if subdata.empty:
            raise Exception(use_valid_reference_string)

        element_data = subdata.squeeze().to_dict()

        return Element(
            symbol=element_data["Symbol"],
            name=element_data["Name"],
            atomic_number=element_data["AtomicNumber"],
            mass=element_data["AtomicMass"],
            color=element_data["Color"],
        )


class OpenGLSphere(OpenGLSurface):
    def __init__(
            self,
            center=ORIGIN,
            **kwargs,
    ):
        super().__init__(
            self.uv_func,
            u_range=(0, TAU),
            v_range=(0, PI),
            **kwargs,
        )

        self.shift(center)

    def uv_func(self, u, v):
        return np.array(
            [np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)],
        )


def mol_parser(file):
    with open(file) as file:
        mol_file = file.readlines()
    # Get general data

    mol_name = mol_file[0].strip()  # This info is not always available  # noqa F841
    mol_source = mol_file[1].strip()  # This info is not always available  # noqa F841
    mol_comments = mol_file[  # noqa F841
        2
    ].rstrip()  # This info is not always available
    mol_general_info = mol_file[3]  # This info is not always available
    mol_file.remove(mol_general_info)  # This info is not always available
    mol_general_info = (
        mol_general_info.rstrip().split()
    )  # This info is not always available
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
            "coords": np.array([x_position, y_position, z_position]),
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
            # "stereo": bond_stereo,
            # "topology": bond_topology,
            # "reacting_center_status": reacting_center_status
        }

        try:
            bond_stereo = line_data[3]
        except Exception as _:
            bond_stereo = ""
        else:
            bond_data["stereo"] = int(bond_stereo)

        try:
            bond_topology = line_data[5]
        except Exception as _:
            bond_topology = ""
        else:
            bond_data["topology"] = int(bond_topology)

        try:
            reacting_center_status = line_data[6]
        except Exception as _:
            reacting_center_status = ""
        else:
            bond_data["reacting_center_status"] = int(reacting_center_status)

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

        if not atoms.get(second_atom_index).get("bond_to"):
            atoms[second_atom_index]["bond_to"] = {
                first_atom_index: atoms.get(first_atom_index).get("element")
            }
        else:
            atoms[second_atom_index]["bond_to"][first_atom_index] = atoms.get(
                first_atom_index
            ).get("element")

    return atoms, bonds  # Should return atoms and bonds


def mol_to_graph(file):
    with open(file) as file:
        mol_file = file.readlines()
    # Get general data

    mol_general_info = mol_file[3]  # This info is not always available
    mol_file.remove(mol_general_info)  # This info is not always available
    mol_general_info = (
        mol_general_info.rstrip().split()
    )  # This info is not always available
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
            "position": np.array([x_position, y_position, z_position]),
            "element": ELEMENT_DICT_ENG[element],
        }

    for line in mol_file[3 + number_of_atoms: 3 + number_of_atoms + number_of_bonds]:
        line_data = line.split()
        first_atom_index = int(float(line_data[0]))
        second_atom_index = int(float(line_data[1]))
        bond_type = line_data[2]
        bonds[(first_atom_index, second_atom_index)] = {"type": bond_type}

    return atoms, bonds  # Should return atoms and bonds
