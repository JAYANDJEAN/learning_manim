import os

from manim import *
from manim.mobject.opengl.opengl_mobject import OpenGLGroup
from manim.mobject.opengl.opengl_surface import OpenGLSurface

from utils import mol_parser, Element, pdb_parser


class OpenGLSphere(OpenGLSurface):
    def __init__(self, center=ORIGIN, **kwargs):
        super().__init__(
            self.uv_func,
            u_range=(0, TAU),
            v_range=(0, PI),
            **kwargs,
        )
        self.shift(center)
        self.scale(0.2)

    def uv_func(self, u, v):
        return np.array([np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)])



class ThreeDMolecule(OpenGLGroup):
    def __init__(self, cords: List = None, **kwargs):
        super().__init__(**kwargs)
        atoms_group = OpenGLGroup()
        for c in cords:
            atoms_group.add(OpenGLSphere(c))

        self.add(atoms_group)
        self.move_to(ORIGIN)


class Atoms(ThreeDScene):
    config.renderer = "opengl"
    config.background_color = "#1C1C1C"

    def construct(self):
        morphine = ThreeDMolecule([ORIGIN, LEFT, RIGHT])
        self.add(morphine)


Atoms().render()
