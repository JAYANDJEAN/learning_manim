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
        self.play(Create(ellipse), Create(dot_focus1), Create(dot_focus2))
        self.wait(time_gap)
        lines = VGroup()
        for x1 in np.linspace(-c + 0.1, c - 0.1, 40):
            y1 = get_y(x1, 'ellipse')
            x2, y2 = get_reflection_line(c, 0, x1, y1, a, b)
            lines.add(Line(np.array([c, 0, 0]),
                           np.array([x1, y1, 0]),
                           stroke_width=1.5))
            lines.add(Line(np.array([x1, y1, 0]),
                           np.array([x2, y2, 0]),
                           stroke_width=1.5))
        lines.set_color_by_gradient(BLUE, YELLOW, RED)
        self.play(Create(lines), run_time=20)
        self.wait(3)
        self.play(FadeOut(lines))
        self.play(FadeOut(dot_focus2), FadeOut(dot_focus1))
        self.wait(time_gap)
        self.play(FadeOut(ellipse, shift=DOWN))
        self.wait(time_gap)
