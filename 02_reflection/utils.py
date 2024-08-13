import numpy as np
from manim import *

a = 5.0
b = 3.0
c = 4.0
r = 3
e = c / a
time_gap = 2


def get_slope_out(k_i, k_n):
    return (2 * k_n - k_i + k_i * np.square(k_n)) / (1 + 2 * k_n * k_i - np.square(k_n))


# ellipse
def get_y(x, long, short):
    return np.sqrt((1 - np.square(x) / np.square(long)) * np.square(short))


def get_slope_normal(x, y, long, short):
    return y * np.square(long) / x / np.square(short)


def get_dual_point(x0, y0, k, long, short):
    A = (np.square(k) / np.square(short) + 1 / np.square(long))
    B = (2 * k * y0 - 2 * np.square(k) * x0) / np.square(short)
    C = (k * x0 - y0) * (k * x0 - y0) / np.square(short) - 1
    discriminant = np.square(B) - 4 * A * C
    x1 = (-B - np.sqrt(discriminant)) / 2 / A
    x2 = (-B + np.sqrt(discriminant)) / 2 / A
    x_p = x2 if np.abs(x1 - x0) < np.abs(x2 - x0) else x1
    y_p = y0 + k * (x_p - x0)
    return x_p, y_p


def get_reflection_line(x0, y0, x1, y1, long, short):
    k_i = (y1 - y0) / (x1 - x0)
    k_n = get_slope_normal(x1, y1, long, short)
    k_o = get_slope_out(k_i, k_n)
    x2, y2 = get_dual_point(x1, y1, k_o, long, short)
    return x2, y2


class SameScene(Scene):
    def __init__(self):
        super().__init__()
        self.plane = NumberPlane(
            background_line_style={
                "stroke_color": "#C2C2C2",
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        )

    def opening(self, title_words):
        self.camera.background_color = "#1C1C1C"

        self.add(self.plane)

        title = Tex(title_words).scale(3)
        self.play(Write(title), run_time=3)
        logo = MathTex(r"\mathbb{JAYANDJEAN}",
                       fill_color="#ece6e2").next_to(title, DOWN, buff=0.5).scale(2)
        self.play(Write(logo), run_time=2)
        self.wait()
        self.play(FadeOut(title))
        self.play(logo.animate.scale(0.4).move_to(RIGHT * 5.4 + UP * 3.2))
        self.wait(2)

    def caption(self, words):
        text = Text(words, font="Sans", font_size=24).move_to(DOWN * 3.5)
        self.play(Write(text), run_time=2)
        return text
