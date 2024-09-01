import glob
import os

from manim import *


class Test(Scene):
    def construct(self):
        jpeg_images = glob.glob(os.path.join("/Users/fengyuan/Desktop/history/*.jpg"))
        images = Group(*[ImageMobject(f) for f in jpeg_images])
        show_time = 7
        animation_list = [
            FadeIn(images[0]),
            FadeOut(images[0]),
            FadeIn(images[1]),
            FadeOut(images[1])
        ]
        self.play(Succession(*animation_list))


class FastSequentialAnimations(Scene):
    def construct(self):
        # 创建几个简单的对象
        circle = Circle()
        square = Square()
        triangle = Triangle()

        # 定义每个对象的创建动画，并加速播放
        animations = [
            Create(circle, run_time=0.5),  # 使用较短的run_time加速动画
            FadeOut(circle),
            Create(square, run_time=0.5),
            Create(triangle, run_time=0.5),
        ]

        # 使用 Succession 按顺序播放动画
        self.play(Succession(*animations))
        self.wait(1)


if __name__ == "__main__":
    scene = Test()
    scene.render()
