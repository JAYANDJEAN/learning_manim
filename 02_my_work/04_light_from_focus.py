from manim import *
from utils.common import *
from utils.template import SameScene
import numpy as np


class Focus(SameScene):
    def construct(self):
        # 片头
        super().opening('Light from Focus')

        ellipse = Ellipse(width=a * 2, height=b * 2, color=BLUE_B)
        dot_focus1 = Dot(color=ORANGE).move_to(RIGHT * c)
        dot_focus2 = Dot(color=ORANGE).move_to(LEFT * c)

        lines = VGroup()
        x0, y0, x1, y1 = c, 0, 2, get_y(2, a, b)
        lines.add(Line(np.array([x0, y0, 0]),
                       np.array([x1, y1, 0]),
                       stroke_width=1.5))
        for i in range(100):
            x2, y2 = get_reflection_line(x0, y0, x1, y1, a, b)
            lines.add(Line(np.array([x1, y1, 0]),
                           np.array([x2, y2, 0]),
                           stroke_width=1.5))
            x0, y0, x1, y1 = x1, y1, x2, y2
        lines.set_color_by_gradient(BLUE, YELLOW, RED)

        # 画椭圆和焦点
        self.play(Create(ellipse), Create(dot_focus1), Create(dot_focus2))
        self.wait(time_gap)
        # 画线
        self.play(Create(lines), run_time=20)
        self.wait(time_gap)
        # 消失
        self.play(FadeOut(lines))
        self.play(FadeOut(dot_focus2), FadeOut(dot_focus1))
        self.wait(time_gap)
        self.play(FadeOut(ellipse, shift=DOWN))
        self.wait(time_gap)
