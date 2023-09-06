from manim import *

class PlayAnimationsInGroup(Scene):
    def construct(self):
        # 创建一个圆和一个正方形
        circle = Circle()
        square = Square()

        # 创建动画对象
        move_circle = circle.animate.shift(UP)
        move_square = square.animate.shift(DOWN)

        # 创建动画组并设置总时长
        group = AnimationGroup(
            Create(circle),
            Create(square),
            move_circle,
            move_square,
            lag_ratio=0.5,  # 调整动画之间的延迟时间
            run_time=3,     # 控制总时长
        )

        # 播放动画组
        self.play(group)