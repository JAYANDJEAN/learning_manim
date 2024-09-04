from manimlib import *
import sys
import os


class RotateCamera(InteractiveScene):
    def construct(self):
        images = ImageMobject("images/image.png")
        self.add(images)
        self.wait(2)
        self.set_floor_plane("xz")
        self.play(self.frame.animate.reorient(-47, -7, 0, (-2.48, 0, -1.09), 7))
        self.wait()
