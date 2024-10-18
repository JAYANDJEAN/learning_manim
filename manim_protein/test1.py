# # 导入 pymol 模块
# from pymol import cmd
from rdkit import Chem
# import pymol
#
# # 启动 PyMOL
# # pymol.finish_launching()
# # 加载一个 PDB 文件
# cmd.load("data/A0A4W3JAN5.pdb")
#
#
# # 选择你想显示的模型（space-filling）
# cmd.show('spheres')
#
# # 保存空间填充模型的坐标数据
# cmd.save('space_filling_model.pdb')


# mol = Chem.MolFromMolFile('data/output_with_bonds.mol')
# mol = Chem.MolFromMolFile('data/morphine3d.mol')
# mol_with_h = Chem.AddHs(mol)
#
# print(len(list(mol_with_h.GetAtoms())))
# print(len(list(mol_with_h.GetBonds())))

mol = Chem.MolFromPDBFile('data/A0A4W3JAN5.pdb')
mol_with_h = Chem.AddHs(mol)
print(len(list(mol_with_h.GetAtoms())))
print(len(list(mol_with_h.GetBonds())))

