from manim import *
import numpy as np


class Reflection(Scene):
    def construct(self):
        PLANE = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 3,
                "stroke_opacity": 0.5
            }
        )
        a = 6.0
        b = 3.0
        ellipse = Ellipse(width=a*2, height=b*2, color=BLUE_B)
        dot0 = Dot(color=ORANGE).move_to(RIGHT * a)
        x0 = 1.0
        y0 = np.sqrt((1 - x0 * x0 / a / a) * b * b)
        k_n = y0 * a * a / x0 / b / b
        k_i = (y0 - 0) / (x0 - a)
        k_o = self.slope_out(k_i, k_n)
        y1 = y0 - k_o * x0
        line1 = Line(dot0, np.array([x0,y0,0]))
        line2 = Line(np.array([x0,y0,0]), np.array([0,y1,0]))

        self.add(PLANE, ellipse, line1, line2)

    def slope_out(self, k_i, k_n):
        return (2 * k_n + k_i * k_n * k_n - k_i) / (1 + 2 * k_n * k_i - k_n * k_n)
