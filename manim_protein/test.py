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
