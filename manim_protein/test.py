
from Bio.PDB import PDBParser
from manim import *


class PDBVisualization(Scene):
    def construct(self):
        parser = PDBParser()
        structure = parser.get_structure('A0A4W3JAN5', 'data/A0A4W3JAN5.pdb')
        atom_group = VGroup()
        scala = 8

        for model in structure:
            for chain in model:
                for residue in chain:
                    print(residue.get_resname())
                    for atom in residue:
                        a = Sphere(radius=0.1)  # Each atom visualized as a small sphere
                        a.move_to(atom.get_coord() / scala)  # Move to its (x, y, z) position
                        a.set_color(BLUE)  # Set color of the atom
                        atom_group.add(a)

        self.add(atom_group)

        # # Optional: Rotate to get a better 3D view
        # self.play(Rotate(atom_group, angle=PI / 4, axis=UP))
        #
        # # Animate the scene
        # self.wait()


PDBVisualization().render()

from manim import *
from threedmolecule import ThreeDMolecule


class Draw3DMorphine(ThreeDScene):
    # Three D Manim Chemistry objects require Opengl renderer
    config.renderer = "opengl"

    def construct(self):
        # OpenGLMobject OpenGLVMobject
        morphine = ThreeDMolecule(filename="data/morphine3d.mol")
        circle_1 = Circle(radius=1.0)
        self.play(Create(morphine))
        self.play(Create(circle_1))
        self.move_camera(phi=75 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation()
        self.wait(5)
        self.stop_ambient_camera_rotation()


Draw3DMorphine().render()

