# # 导入 pymol 模块
from pymol import cmd
import pymol

cmd.load("data/A0A4W3JAN5_min.pdb")
cmd.h_add()
cmd.save("data/A0A4W3JAN5_min.mol", format="mol")
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



