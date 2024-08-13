from manim import *
from utils import *
import numpy as np


def get_lines_for_reflection(num_points, long, short):
    lines = VGroup()
    actions = []
    width = 1.5 if num_points > 100 else 3
    run = 7 if num_points > 100 else 3

    for i in range(1, num_points):
        theta = i * 2 * PI / num_points
        x1 = Circle(radius=long).point_at_angle(theta)[0]
        for y1 in [get_y(x1, long, short), -get_y(x1, long, short)]:
            x2, y2 = get_reflection_line(long, 0, x1, y1, long, short)
            line1 = Line(np.array([long, 0, 0]),
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
        super().opening('Reflection II')

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

        circle = Circle(radius=r, color=BLUE_B, stroke_width=3)
        dot = Dot(color=ORANGE).move_to(r * RIGHT)

        # 画圆和点
        text = super().caption("我们先从简单的例子出发，可视化光线在圆里的反射。")
        self.play(Create(circle), Create(dot))
        self.wait(time_gap)

        # 画示例光线
        self.play(FadeOut(text))
        text = super().caption("光线经圆的内壁反射，比如像这样。")
        actions1, lines1 = get_lines_for_reflection(num_demo, r, r)
        self.play(*actions1)
        self.wait(time_gap)

        # 示例光线消失
        self.play(FadeOut(lines1), FadeOut(text))
        self.wait(time_gap)
        # 画全部光线
        text = super().caption("增加光线数量，以模拟真实场景。")
        actions2, lines2 = get_lines_for_reflection(num_all, r, r)
        self.play(*actions2)
        self.wait(time_gap)

        # 画极坐标图像
        self.play(FadeOut(text))
        text = super().caption("光线形成的包络是心脏线。")
        self.play(Create(cardioid), run_time=4)

        # 消失
        self.play(FadeOut(circle, dot, lines2), FadeOut(text))
        self.wait(time_gap)
        self.play(FadeOut(cardioid))
        self.wait(time_gap)

        ellipse = Ellipse(width=a * 2, height=b * 2, color=BLUE_B)
        dot = Dot(color=ORANGE).move_to(a * RIGHT)
        # 画椭圆
        text = super().caption("现在可视化光线在椭圆内的反射。")
        self.play(Create(ellipse), Create(dot))
        self.wait(time_gap)
        # 画全部光线
        actions2, lines2 = get_lines_for_reflection(num_all, a, b)
        self.play(*actions2)
        self.wait(time_gap)
        # 消失
        self.play(FadeOut(lines2), FadeOut(text))
        self.wait(time_gap)

        text = super().caption("这个形成的包络是什么曲线呢？")
        self.wait(time_gap)

        self.play(FadeOut(text))
        self.play(FadeOut(ellipse, shift=DOWN), FadeOut(dot, shift=DOWN))
        self.wait(time_gap)
