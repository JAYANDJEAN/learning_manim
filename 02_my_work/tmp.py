from manim import *
from utils.template import SameScene


class PlayAnimationsInGroup(SameScene):
    def construct(self):
        super().opening("Point Light in Ellipse")
        # 创建一个圆和一个正方形
        circle = Circle()
        square = Square()

        # 播放动画组
        self.play(Create(circle))
        self.wait(2)
