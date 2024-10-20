from manim import *

from threedmolecule import ThreeDMolecule


class Draw3DMorphine(ThreeDScene):
    config.renderer = "opengl"
    config.background_color = "#1C1C1C"

    def construct(self):
        morphine = ThreeDMolecule(filename="data/morphine3d.mol")
        self.play(Create(morphine, run_time=3))
        self.move_camera(phi=75 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()


class ProteinRibbonDiagram(ThreeDScene):
    def construct(self):
        # 使用3D场景
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # 示例点列表示蛋白质的主链
        points = [
            np.array([0, 0, 0]),
            np.array([1, 2, 1]),
            np.array([2, 1, 2]),
            np.array([3, 3, 3]),
            np.array([4, 0, 4]),
        ]

        # 创建曲线并将点平滑连接
        ribbon = VMobject()
        ribbon.set_points_smoothly(points)
        ribbon.set_color(BLUE)

        # 添加曲线
        self.add(ribbon)


# ProteinRibbonDiagram().render()
