from manim import *
from utils.common import *
from utils.template import Opening


class Focus(Opening):
    def construct(self):
        # 片头
        super().construct()

        ellipse = Ellipse(width=a * 2, height=b * 2, color=BLUE_B)
        dot_focus1 = Dot(color=ORANGE).move_to(RIGHT * c)
        dot_focus2 = Dot(color=ORANGE).move_to(LEFT * c)
        self.play(Create(ellipse), Create(dot_focus1), Create(dot_focus2))
        self.wait(time_gap)

