# 文件格式说明

**Author:** ChatGPT

## PDB文件说明

### HEADER 行的解释
```yaml
HEADER                                            01-JUN-22
```
1. HEADER 是 PDB 文件的文件头部分，用于简要描述文件内容以及文件的发布日期。
2. 01-JUN-22：表示该 PDB 文件创建的日期是 2022 年 6 月 1 日。
3. 空白部分：通常用于描述结构的类别或简要说明，但在此处为空，可能是因为文件的创建者选择不填写。

### TITLE 行的解释
```yaml
TITLE     ALPHAFOLD MONOMER V2.0 PREDICTION FOR PROTEIN KINASE DOMAIN-
TITLE    2 CONTAINING PROTEIN (A0A4W3JAN5)
```
1. TITLE 提供了关于该结构的标题信息，通常包含了结构的名字、来源或研究背景。这一段可以跨多行出现，标号 2 表示第二行。
2. ALPHAFOLD MONOMER V2.0 PREDICTION：说明该结构是通过 AlphaFold Monomer V2.0 模型预测的。AlphaFold 是由 DeepMind 开发的用于蛋白质结构预测的 AI 模型，这表明该 PDB 文件并非通过实验获得的结构，而是基于 AlphaFold 的计算机预测。
3. PROTEIN KINASE DOMAIN-CONTAINING PROTEIN：这是该蛋白质的功能或类型描述，表明该蛋白质包含蛋白激酶（protein kinase）结构域。蛋白激酶是一类重要的酶，负责催化磷酸基团转移过程。
4. A0A4W3JAN5：这是蛋白质的 UniProt ID，表示该蛋白的唯一标识符。在 UniProt 数据库中，A0A4W3JAN5 对应一种具体的蛋白质序列，通常用于研究人员定位蛋白质的详细信息。
结合含义
5. 这段信息表明，文件描述了一个蛋白质的三维结构，该蛋白质包含蛋白激酶结构域。其结构是通过 AlphaFold Monomer V2.0 模型预测的，并非通过实验获得。蛋白质的唯一标识符（UniProt ID）为 A0A4W3JAN5，可以通过这个 ID 在 UniProt 数据库中找到该蛋白质的详细信息。

### COMPND 行的解释
```yaml
COMPND   2 MOLECULE: PROTEIN KINASE DOMAIN-CONTAINING PROTEIN;
COMPND   3 CHAIN: A
```
1. COMPND（Compound，化合物）部分描述了结构中的分子信息。
2. MOLECULE：该字段表明了蛋白质的名称或类型。
3. PROTEIN KINASE DOMAIN-CONTAINING PROTEIN：说明该蛋白质包含 蛋白激酶结构域。蛋白激酶结构域是催化磷酸基团从 ATP 转移到特定氨基酸（如丝氨酸、苏氨酸或酪氨酸）上的区域，这在细胞信号传导和调节中起关键作用。
4. CHAIN: A：表明该结构中的一条多肽链标识为 链 A。PDB 文件通常使用字母来标识结构中的不同链（如 A、B 等），在这里表明该蛋白质结构只有一条链。

### SOURCE 行的解释
```yaml
SOURCE    MOL_ID: 1;
SOURCE   2 ORGANISM_SCIENTIFIC: CALLORHINCHUS MILII;
SOURCE   3 ORGANISM_TAXID: 7868
```
1. SOURCE（来源）部分描述了该蛋白质分子的生物来源。
2. MOL_ID: 1：指明该分子的编号为 1，在这个上下文中意味着这个文件描述的唯一分子是编号为 1 的蛋白质分子。
3. ORGANISM_SCIENTIFIC: CALLORHINCHUS MILII：描述了蛋白质的来源物种，Callorhinchus milii 是学名，指的是银鲛（也叫澳洲银鲛），一种软骨鱼类。银鲛是一种原始的脊椎动物，常用作进化和发育研究的模型生物。
4. ORGANISM_TAXID: 7868：这是物种在 NCBI（国家生物技术信息中心） 的 Taxonomy ID（分类 ID），编号 7868 对应 Callorhinchus milii。研究人员可以通过这个 ID 在 NCBI 数据库中找到该物种的详细分类和相关信息。

### SEQRES 行的解释
```yaml
SEQRES   1 A  330  MET GLU ASN PHE GLN LYS VAL GLU LYS ILE GLY GLU GLY          
SEQRES   2 A  330  THR TYR GLY VAL VAL TYR LYS ALA ARG ASN LYS LEU THR          
SEQRES   3 A  330  GLY GLU VAL VAL ALA LEU LYS LYS ILE ARG LEU ASP THR          
SEQRES   4 A  330  GLU THR GLU GLY VAL PRO SER THR ALA ILE ARG GLU ILE          
SEQRES   5 A  330  SER LEU LEU LYS GLU LEU SER HIS PRO ASN ILE VAL LYS          
SEQRES   6 A  330  LEU LEU ASP VAL ILE HIS THR GLU ASN LYS LEU TYR LEU          
SEQRES   7 A  330  VAL PHE GLU PHE LEU HIS GLN ASP LEU LYS LYS PHE MET          
SEQRES   8 A  330  ASP VAL SER SER VAL GLY GLY ILE PRO LEU PRO LEU VAL          
SEQRES   9 A  330  LYS SER TYR LEU TYR GLN LEU LEU GLN GLY LEU ALA PHE          
SEQRES  10 A  330  CYS HIS SER HIS ARG VAL LEU HIS ARG ASP LEU LYS PRO          
SEQRES  11 A  330  GLN ASN LEU LEU ILE ASN ALA ASP GLY ALA ILE LYS LEU          
SEQRES  12 A  330  ALA ASP PHE GLY LEU ALA ARG ALA PHE GLY VAL PRO VAL          
SEQRES  13 A  330  ARG THR TYR THR HIS GLU VAL VAL THR LEU TRP TYR ARG          
SEQRES  14 A  330  ALA PRO GLU ILE LEU LEU GLY CYS LYS TYR TYR SER THR          
SEQRES  15 A  330  ALA VAL ASP ILE TRP SER LEU GLY CYS ILE PHE ALA GLU          
SEQRES  16 A  330  MET LEU GLU PRO ILE LEU LEU ASP SER ARG GLN ASN LEU          
SEQRES  17 A  330  HIS CYS CYS GLY SER LYS LEU LEU ASN LEU PRO GLY LEU          
SEQRES  18 A  330  SER LEU ARG PHE THR GLU PRO ILE THR ARG ARG ALA LEU          
SEQRES  19 A  330  PHE PRO GLY ASP SER GLU ILE ASP GLN LEU PHE ARG ILE          
SEQRES  20 A  330  PHE ARG THR LEU GLY THR PRO ASP GLU GLY VAL TRP PRO          
SEQRES  21 A  330  GLY VAL SER ALA MET PRO ASP TYR LYS HIS THR PHE PRO          
SEQRES  22 A  330  ARG TRP SER ARG GLN GLU LEU SER LYS VAL VAL PRO PRO          
SEQRES  23 A  330  LEU GLY GLU GLY GLY ARG ASP LEU LEU ALA GLN MET LEU          
SEQRES  24 A  330  LEU TYR ASP PRO THR GLU ARG VAL SER ALA LYS THR ALA          
SEQRES  25 A  330  ILE SER HIS LEU PHE PHE GLN ASP VAL THR THR ALA ILE          
SEQRES  26 A  330  PRO HIS LEU ARG VAL 
```
1. SEQRES：表示该记录是序列记录。
2. n：表示这是该序列的第几行。PDB 文件中，每行最多可以容纳 13 个氨基酸，超过 13 个时会继续写到下一行。因此，序列通常分为多行记录。
3. A：代表该序列属于 链 A，这是 PDB 文件中的链标识符。
4. 330：表示链 A 的总共长度为 330 个氨基酸。
5. <amino acids>：每行记录一部分氨基酸序列，氨基酸用其三个字母的缩写表示。
6. 该记录展示了蛋白质链 A 的完整氨基酸序列，包含 330 个氨基酸。这是蛋白质结构中所有构成该链的残基。
7. SEQRES 记录中列出的氨基酸序列是基于原始蛋白质序列，它表示蛋白质的一级结构（氨基酸序列），与三维结构相关但并不直接代表空间中的位置。
8. 结合 PDB 文件的三维结构信息，可以分析氨基酸在蛋白质中的具体位置及其在折叠后的空间结构中如何相互作用。
9. SEQRES 记录是重要的基础信息，后续的 ATOM 记录则具体描述每个氨基酸残基的三维坐标和其构成的原子信息。

#### 氨基酸
1. MET 是氨基酸 甲硫氨酸（Methionine） 的三字母缩写。在 SEQRES 记录的第一行中，MET 出现在序列的起始位置，表示链 A 的第一个氨基酸是甲硫氨酸。这符合蛋白质合成的常见生物学规律，即以甲硫氨酸作为起始氨基酸。
2. 甲硫氨酸（Methionine，简称 MET）的化学式是： C₅H₁₁NO₂S
3. 甲硫氨酸的结构特点： 
   1. 氨基（NH₂）基团：和所有氨基酸一样，甲硫氨酸含有一个氨基团（-NH₂）。
   2. 羧基（COOH）基团：也含有一个羧基团（-COOH），是氨基酸的酸性部分。
   3. 侧链：甲硫氨酸的独特之处在于其侧链含有一个 硫醚基团（-S-CH₃），其化学结构为 CH₂-CH₂-S-CH₃。这使得甲硫氨酸具有含硫的特性。

### 坐标系
```yaml
CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1          
ORIGX1      1.000000  0.000000  0.000000        0.00000                         
ORIGX2      0.000000  1.000000  0.000000        0.00000                         
ORIGX3      0.000000  0.000000  1.000000        0.00000                         
SCALE1      1.000000  0.000000  0.000000        0.00000                         
SCALE2      0.000000  1.000000  0.000000        0.00000                         
SCALE3      0.000000  0.000000  1.000000        0.00000        
```
1. CRYST1 记录描述晶胞（unit cell）的参数和晶体对称性。具体含义为：
   1. 1.000 1.000 1.000：分别表示晶胞的三个边长，即 a、b 和 c，单位是 Å（埃，1 Å = 10⁻¹⁰ 米）。在这里，晶胞的三个边长都是 1.000 Å。
   2. 90.00 90.00 90.00：表示晶胞的三个夹角，分别是 α、β 和 γ（即晶胞的角度）。在此，所有角度都是 90 度，表示该晶胞是一个正交晶系的立方结构。
   3. P 1：这是晶体对称性描述，表示晶体的空间群（space group）。P 表示该晶体是原子排列在简单立方格子上，而 1 表示最低对称性，空间群是最简单的无对称操作。
   4. 1：指空间群号，1 是 P1 的编号，表示最简单的三维晶格结构，没有任何旋转或反演对称性。
2. ORIGXn 记录定义了原始坐标系到标准坐标系的转换矩阵。每一行对应一个坐标轴的变换系数和偏移量：
   1. 这些表示从原始坐标系到标准坐标系的线性变换矩阵。由于系数是单位矩阵且偏移量为零，这里表示没有任何坐标系变换，坐标系保持原样。
3. SCALEn 记录提供了晶胞内坐标系的缩放系数，即将原始坐标（Cartesion 坐标）缩放到单位晶胞（fractional 坐标）中的转换矩阵。
   1. 这些矩阵意味着晶体的坐标没有被缩放或改变，保持单位长度。

### Model
```yaml
MODEL        1                                                                  
ATOM      1  N   MET A   1     -19.514   9.408  21.651  1.00 83.00           N  
ATOM      2  CA  MET A   1     -18.255   9.343  22.440  1.00 83.00           C  
ATOM      3  C   MET A   1     -18.464   8.854  23.873  1.00 83.00           C  
ATOM      4  CB  MET A   1     -17.485  10.675  22.434  1.00 83.00           C  
ATOM      5  O   MET A   1     -17.529   8.294  24.427  1.00 83.00           O  
ATOM      6  CG  MET A   1     -16.670  10.847  21.144  1.00 83.00           C  
ATOM      7  SD  MET A   1     -15.438   9.546  20.833  1.00 83.00           S  
ATOM      8  CE  MET A   1     -14.201   9.917  22.102  1.00 83.00           C  
.
.
.
```
1. MODEL 记录用于指示当前模型的编号。在这个例子中，模型的编号是 1。在一些多模型结构中，这个记录用来区分不同的模型，比如在分子动力学模拟或不同构象中。
2. ATOM：标识这是一个原子记录。
3. 1：原子的序号（编号），在这个例子中是 1。
4. N：原子的名称，这里是氮原子（N）。
5. MET：残基名称，这里是甲硫氨酸（Methionine，MET）。
6. A：链标识符，表示这个原子属于链 A。
7. 1：残基序号，表示这是链 A 中的第 1 个残基。
8. -19.514 9.408 21.651：原子的三维坐标，分别表示 x、y 和 z 坐标，单位是 Å（埃）。
9. 1.00：占有率，表示该原子在该位置的存在概率，通常在 1.00 表示完全占有。
10. 83.00：AlphaFold 生成每个残基的模型置信度分数（pLDDT），范围在 0 到 100 之间。一些 pLDDT 低于 50 的区域可能在孤立状态下是无结构的
11. N：原子的元素符号，这里是氮（N）。

### TER 记录解析
```yaml
TER    2632      VAL A 330
```
1. TER：表示这是一个终止记录，用于指示一个多肽链的结束。它通常用在链的最后一个残基之后，以便于解析和可视化。
2. 2632：这个数字是当前记录的序号，通常是原子的序号或标识符，但在 TER 记录中，它仅用作标识，没有其他含义。
3. VAL：残基的名称，这里是缬氨酸（Valine）。
4. A：链标识符，表示这个残基属于链 A。
5. 330：残基序号，表示这是链 A 中的第 330 个残基。

## MOL文件