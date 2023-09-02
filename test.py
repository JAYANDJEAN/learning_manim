from manim import *

class HorizontalLineExample(Scene):
    def construct(self):
        # 创建坐标系
        axes = Axes(
            x_range=[-5, 5],
            y_range=[-2, 2],
            axis_config={"color": BLUE},
        )
        self.play(Create(axes))

        # 创建一个水平线
        horizontal_line = axes.get_horizontal_line((1,2,0), color=GREEN)

        # 在坐标系中添加水平线
        self.play(Create(horizontal_line))

        self.wait(2)