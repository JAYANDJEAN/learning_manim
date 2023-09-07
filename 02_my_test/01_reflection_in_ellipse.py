from manim import *
from utils.common import *
from utils.template import Opening


class Reflection(Opening):
    def construct(self):
        # 片头

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
