from manim import *
from utils.template import Opening


class PlayAnimationsInGroup(Opening):
    def construct(self):
        super().construct()
        # 创建一个圆和一个正方形
        circle = Circle()
        square = Square()

        # 播放动画组
        self.play(Create(circle))
        self.wait(2)
