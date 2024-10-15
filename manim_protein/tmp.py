from Bio.PDB import PDBParser

# 创建解析器
parser = PDBParser()

# 解析结构
structure = parser.get_structure('A0A4W3JAN5', '1abc.pdb')

# 遍历所有链和残基
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                print(atom.get_name(), atom.get_coord())
