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
        ellipse = Ellipse(width=a * 2, height=b * 2, color=BLUE_B)
        dot0 = Dot(radius=0.01, color=ORANGE).move_to(RIGHT * a)
        x0 = -3
        y0 = self.get_y(x0, a, b)
        k_n = self.get_slope_n(x0, y0, a, b)
        k_i = (y0 - 0) / (x0 - a)
        k_o = self.get_slope_out(k_i, k_n)
        x1, y1 = self.get_another_point(x0, y0, k_o, a, b)
        line1 = Line(dot0, np.array([x0, y0, 0]))
        line2 = Line(np.array([x0, y0, 0]), np.array([x1, y1, 0]))

        self.add(PLANE, ellipse, line1, line2)

    def get_slope_n(self, x, y, a, b):
        return y * a * a / x / b / b

    def get_slope_out(self, k_i, k_n):
        return (2 * k_n + k_i * k_n * k_n - k_i) / (1 + 2 * k_n * k_i - k_n * k_n)

    def get_y(self, x, a, b):
        return np.sqrt((1 - x * x / a / a) * b * b)

    def get_another_point(self, x0, y0, k, a, b):
        A = (k * k / b / b + 1 / a / a)
        B = (2 * k * y0 - 2 * k * k * x0) / b / b
        C = (k * x0 - y0) * (k * x0 - y0) / b / b - 1
        x1 = (-B - np.sqrt(B * B - 4 * A * C)) / 2 / A
        y1 = self.get_y(x1, a, b)
        return x1, y1
