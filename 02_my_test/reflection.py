from manim import *
import numpy as np

a = 5.0
b = 3.0
c = np.sqrt(np.square(a) - np.square(b))
time_gap = 2


def get_slope_out(k_i, k_n):
    return (2 * k_n - k_i + k_i * np.square(k_n)) / (1 + 2 * k_n * k_i - np.square(k_n))


# ellipse
def get_ellipse_y(x):
    return np.sqrt((1 - np.square(x) / np.square(a)) * np.square(b))


def get_ellipse_slope_n(x, y):
    return y * np.square(a) / x / np.square(b)


def get_ellipse_another_point(x0, y0, k):
    A = (np.square(k) / np.square(b) + 1 / np.square(a))
    B = (2 * k * y0 - 2 * np.square(k) * x0) / np.square(b)
    C = (k * x0 - y0) * (k * x0 - y0) / np.square(b) - 1
    x1 = (-B - np.sqrt(np.square(B) - 4 * A * C)) / 2 / A
    x2 = (-B + np.sqrt(np.square(B) - 4 * A * C)) / 2 / A
    x_p = x2 if np.abs(x1 - x0) < np.abs(x2 - x0) else x1
    y_p = y0 + k * (x_p - x0)
    return x_p, y_p


def get_ellipse_reflections(x_ellipse, y_ellipse, num):
    k_i = (y_ellipse - b) / x_ellipse
    lines = VGroup()
    lines.add(Line(np.array([0, b, 0]),
                   np.array([x_ellipse, y_ellipse, 0]),
                   stroke_width=1.5))
    for i in range(num):
        k_n = get_ellipse_slope_n(x_ellipse, y_ellipse)
        k_o = get_slope_out(k_i, k_n)
        x1, y1 = get_ellipse_another_point(x_ellipse, y_ellipse, k_o)

        lines.add(Line(np.array([x_ellipse, y_ellipse, 0]),
                       np.array([x1, y1, 0]),
                       stroke_width=1.5))
        x_ellipse = x1
        y_ellipse = y1
        k_i = k_o
    lines.set_color_by_gradient(BLUE, YELLOW, RED)
    return lines


class Reflection(Scene):
    def construct(self):
        # 片头
        PLANE = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        )
        self.add(PLANE)
        title = Tex("Reflection in Ellipse").scale(3)
        self.play(Write(title), run_time=3)
        logo = MathTex(r"\mathbb{JAYANDJEAN}", fill_color="#343434").next_to(title, DOWN, buff=0.5).scale(2)
        self.play(Write(logo), run_time=2)
        self.wait()
        self.play(FadeOut(title))
        self.play(logo.animate.scale(0.4).move_to(RIGHT * 5.4 + UP * 3.2))
        self.wait(2)

        # 项目
        ellipse = Ellipse(width=a * 2, height=b * 2, color=BLUE_B)
        dot_focus1 = Dot(color=ORANGE).move_to(RIGHT * c)
        dot_focus2 = Dot(color=ORANGE).move_to(LEFT * c)
        self.play(Create(ellipse), Create(dot_focus1), Create(dot_focus2))
        self.wait(time_gap)

        x_list = [2.0, 3.0, 4.0, 4.5, 4.95]
        for x in x_list:
            lines = get_ellipse_reflections(x, -get_ellipse_y(x), 100)
            self.play(Create(lines), run_time=7)
            self.wait(time_gap)
            self.play(FadeOut(lines))
            self.wait(time_gap)
            if x == 4.95:
                lines = get_ellipse_reflections(x, get_ellipse_y(x), 100)
                self.play(Create(lines), run_time=7)
                self.wait(time_gap)
                self.play(FadeOut(lines))
                self.wait(time_gap)
        self.play(FadeOut(dot_focus2), FadeOut(dot_focus1))
        self.wait(time_gap)
        self.play(FadeOut(ellipse, shift=DOWN))
        self.wait(time_gap)
