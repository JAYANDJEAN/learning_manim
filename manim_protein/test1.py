# 导入 pymol 模块
from pymol import cmd

# 加载一个 PDB 文件
cmd.load("data/A0A4W3JAN5.pdb", "molecule_name")

# 为分子添加氢原子
cmd.h_add("molecule_name")

# 保存带有氢原子的分子到新的 PDB 文件
cmd.save("data/molecule_with_hydrogen.pdb", "molecule_name")

# 可选：可视化显示氢原子
cmd.show("spheres", "hydro")  # 显示氢原子为球
cmd.show("sticks", "molecule_name")  # 显示其他原子为棒状结构

# 如果需要，退出 PyMOL
cmd.quit()