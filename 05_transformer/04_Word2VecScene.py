from manim import *


class LabeledArrowIn3D(ThreeDScene):
    def construct(self):
        # 设置 3D 坐标系
        axes = ThreeDAxes()
        arrow = LabeledArrow(".", start=ORIGIN, end=RIGHT * 3 + UP * 2 + OUT, label_position=0.5)
        label = always_redraw(Text("label").next_to(arrow.get_top()))
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, arrow, label)
        self.begin_ambient_camera_rotation(rate=0.1)  # 让摄像机旋转以展示 3D 效果
        self.wait(5)


if __name__ == "__main__":
    scene = LabeledArrowIn3D()
    scene.render()
