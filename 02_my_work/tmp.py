import numpy as np
from manim import *
from utils.common import *
from utils.template import SameScene


class HyperbolaScene(Scene):
    def construct(self):
        plane = PolarPlane()

        graph = plane.plot_polar_graph(
            lambda theta: 1 / (1 + e * np.cos(theta)),
            theta_range=[0, 2 * PI],
            color=ORANGE)
        self.add(plane, graph)
        self.wait(3)
