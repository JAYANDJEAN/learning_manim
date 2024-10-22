from manim import *
from manim_chemistry import *


class Draw3DMorphine(ThreeDScene):
    config.renderer = "opengl"

    def construct(self):
        three_d_morphine = ThreeDMolecule.from_mol_file("data/morphine3d.mol", "data/Elementos.csv")
        self.add(three_d_morphine)


Draw3DMorphine().render()
