from manim import *

from threedmolecule import ThreeDMolecule


class Draw3DMorphine(ThreeDScene):
    config.renderer = "opengl"
    config.background_color = "#1C1C1C"

    def construct(self):
        morphine = ThreeDMolecule(filename="data/morphine3d.mol")
        self.play(Create(morphine, run_time=3))
        self.move_camera(phi=75 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()


