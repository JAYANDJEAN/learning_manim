from manim import *
from utils.common import *
from utils.template import SameScene
import numpy as np


def get_lines_for_reflection(num_points):
    lines = VGroup()
    actions = []
    width = 1.5 if num_points > 100 else 3
    run = 7 if num_points > 100 else 4

    for i in range(1, num_points):
        theta = i * 2 * PI / num_points
        x1 = Circle(radius=r).point_at_angle(theta)[0]
        for y1 in [get_y(x1, r, r), -get_y(x1, r, r)]:
            x2, y2 = get_reflection_line(r, 0, x1, y1, r, r)
            line1 = Line(np.array([r, 0, 0]),
                         np.array([x1, y1, 0]),
                         stroke_width=width,
                         color=GREY)
            line2 = Line(np.array([x1, y1, 0]),
                         np.array([x2, y2, 0]),
                         stroke_width=width,
                         color=GREY)
            actions.append(Create(VGroup(line1, line2), run_time=run))
            lines.add(line1)
            lines.add(line2)
    return actions, lines


class Point(SameScene):
    def __init__(self):
        super().__init__()

    def construct(self):
        # 片头
        super().opening('Point Light in Circle')

        num_demo = 8
        num_all = 128
        cardioid = self.plane.plot_parametric_curve(
            lambda t: np.array(
                [2 * (1 + np.cos(t)) * np.cos(t) - 1,
                 2 * (1 + np.cos(t)) * np.sin(t),
                 0]
            ),
            t_range=[0, TAU],
            color=WHITE,
        )

        circle = Circle(radius=r, color=WHITE, stroke_width=3)
        dot = Dot(color=ORANGE).move_to(r * RIGHT)

        # 画圆和点
        self.play(Create(circle), Create(dot))
        self.wait(time_gap)

        # 画示例光线
        actions1, lines1 = get_lines_for_reflection(num_demo)
        self.play(*actions1)
        self.wait(time_gap)

        # 示例光线消失
        self.play(FadeOut(lines1))
        self.wait(time_gap)

        # 画全部光线
        actions2, lines2 = get_lines_for_reflection(num_all)
        self.play(*actions2)
        self.wait(time_gap)

        # 画极坐标图像
        self.play(Create(cardioid), run_time=4)

        #
        self.play(FadeOut(circle, dot, lines2))
        self.wait(time_gap)

        self.play(FadeOut(cardioid))
        self.wait(time_gap)
