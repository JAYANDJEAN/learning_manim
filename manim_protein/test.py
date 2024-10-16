from manim import *
from manim_chemistry import (
    MMoleculeObject,
    GraphMolecule,
    ThreeDMolecule,
    MElementObject,
    PeriodicTable,
    Orbital,
    BohrAtom,
)


class Draw3DMorphine(ThreeDScene):
    # Three D Manim Chemistry objects require Opengl renderer
    config.renderer = "opengl"

    def construct(self):
        morphine = ThreeDMolecule.from_mol_file(
            filename="data/morphine3d.mol",
            source_csv="data/Elementos.csv",
        )
        self.play(Create(morphine))
        self.move_camera(phi=75 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation()
        self.wait(5)
        self.stop_ambient_camera_rotation()


Draw3DMorphine().render()
