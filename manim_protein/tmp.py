from manim import *
from manim_chemistry import *


class Draw3DMorphine(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-3, 4, 1],  # x轴范围
            y_range=[-3, 3, 1],  # y轴范围
            z_range=[-3, 3, 1],  # z轴范围
            x_length=5,
            y_length=5,
            z_length=5,
        )
        # 添加坐标轴标签
        x_label = axes.get_x_axis_label(Text("x"), edge=OUT + RIGHT, direction=OUT)
        y_label = axes.get_y_axis_label(Text("y"), edge=OUT + UP, direction=OUT)
        z_label = axes.get_z_axis_label(Text("z"), direction=OUT)

        # 创建摄像机，并调整角度
        self.set_camera_orientation(phi=90 * DEGREES, theta=90 * DEGREES, gamma=0 * DEGREES)
        self.add(axes, x_label, y_label, z_label)


Draw3DMorphine().render()
