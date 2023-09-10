import numpy as np
from manim import *
from utils.common import *
from utils.template import SameScene


def get_ellipse_reflections(x_start, y_start, num):
    x0, y0, x1, y1 = 0, b, x_start, y_start
    lines = VGroup()
    lines.add(Line(np.array([x0, y0, 0]),
                   np.array([x1, y1, 0]),
                   stroke_width=1.5))
    for i in range(num):
        x2, y2 = get_reflection_line(x0, y0, x1, y1, a, b)
        lines.add(Line(np.array([x1, y1, 0]),
                       np.array([x2, y2, 0]),
                       stroke_width=1.5))
        x0, y0, x1, y1 = x1, y1, x2, y2
    lines.set_color_by_gradient(BLUE, YELLOW, RED)
    return lines


class Hyper(SameScene):
    def __init__(self):
        super().__init__()

    def construct(self):
        # 片头
        super().opening("Reflection in Ellipse")

        hyperbola = self.plane.plot_parametric_curve(
            lambda t: np.array(
                [5 * np.cosh(t),
                 2 * np.sinh(t),
                 0]
            ),
            t_range=[-2, 2],
            color=WHITE,
        )
        self.play(Create(hyperbola), run_time=4)
        self.wait(time_gap)
