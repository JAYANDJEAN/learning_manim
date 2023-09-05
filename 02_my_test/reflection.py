from manim import *


class Reflection(Scene):
    def construct(self):
        PLANE = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 3,
                "stroke_opacity": 0.5
            }
        )
        ellipse = Ellipse(width=6.0, height=3.0, color=BLUE_B)

        self.add(PLANE, ellipse)

    def slope_out(self, k_i, k_n):
        return (2 * k_n + k_i * k_n * k_n - k_i) / (1 + 2 * k_n * k_i - k_n * k_n)
