from helpers import *


class LabeledArrowIn3D(ThreeDScene):
    def construct(self):
        im = ImageMobject("assets/image.png").scale(0.1)
        axes = ThreeDAxes()
        arrow = ArrowWithLabel(
            axes.get_origin(),
            [2, 1, 3],
            stroke_width=1.5,
            stroke_color=YELLOW,
            label=Text('label', font_size=14),
            buff=0,
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES, frame_center=2 * LEFT)
        self.add(axes, arrow, arrow.label)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)


if __name__ == "__main__":
    scene = LabeledArrowIn3D()
    scene.render()
