from Bio.PDB import PDBParser

# 创建解析器
parser = PDBParser()

# 解析结构
structure = parser.get_structure('A0A4W3JAN5', 'data/A0A4W3JAN5.pdb')

# 遍历所有链和残基
for model in structure:
    for chain in model:
        for residue in chain:
            print(residue.get_resname())
            for atom in residue:
                print(atom.get_name(), atom.get_coord(), atom.get_bfactor(), atom.get_occupancy())
