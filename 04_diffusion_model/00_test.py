from utils import *

from manim import *


# class RotateCamera(ThreeDCamera):
#     def construct(self):
#         self.set_floor_plane("xz")
#         self.play(frame.animate.reorient(-47, -7, 0, (-2.48, -5.84, -1.09), 20))
#         self.wait()


class TwoAndThreeDimensionalScene(ThreeDScene):
    def construct(self):
        # 创建二维坐标系，并移动到左侧
        plane = NumberPlane()
        plane.move_to(LEFT * 4)  # 移动到画布左侧

        # 创建三维坐标系，并移动到右侧
        axes_3d = ThreeDAxes()
        axes_3d.move_to(RIGHT * 4)  # 移动到画布右侧

        # 将坐标系添加到场景中
        self.add(plane)
        self.add(axes_3d)

        # 如果需要显示3D视角，则进入3D模式
        self.begin_ambient_camera_rotation(rate=0.1)  # 可选的，使摄像机缓慢旋转以查看3D坐标系

        # 暂停几秒以便观察
        self.wait(3)

        # 停止3D相机旋转
        self.stop_ambient_camera_rotation()


class RotateCameraExample(ThreeDScene):
    def construct(self):
        # image_prompt = ImageMobject("assets/prompt.png").set(height=4)
        # rect = SurroundingRectangle(image_prompt, buff=0.0)
        # image = Group(image_prompt, rect)
        # 是image太大了，所以效果不好
        im = VGroup(Circle(), Rectangle(), Triangle())

        self.play(Animation(im))
        self.move_camera(phi=-50 * DEGREES,
                         theta=-140 * DEGREES,
                         gamma=-37 * DEGREES,
                         focal_distance=30,
                         frame_center=LEFT + DOWN * 0.3,
                         run_time=3)
        self.begin_3dillusion_camera_rotation()
        self.wait(3)
        self.stop_3dillusion_camera_rotation()


class CameraAnglesAnimation(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=(-6, 6, 1),
            y_range=(-6, 6, 1),
            z_range=(-6, 6, 1),
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={
                "include_tip": True,
                "numbers_to_include": np.arange(-5, 6, 2),
                "font_size": 24,
            },
        )
        x_label = Text("X", font_size=24).next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("Y", font_size=24).next_to(axes.y_axis.get_end(), UP)
        z_label = Text("Z", font_size=24).next_to(axes.z_axis.get_end(), OUT)

        angle_text = always_redraw(
            lambda: Text(f"phi: {self.camera.get_phi() / PI * 180:.2f}, "
                         f"theta: {self.camera.get_theta() / PI * 180:.2f}, "
                         f"gamma: {self.camera.get_gamma() / PI * 180:.2f}").scale(0.3).to_edge(UP + LEFT)
        )

        gap = 10
        self.add_fixed_in_frame_mobjects(angle_text)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, x_label, y_label, z_label)
        self.begin_ambient_camera_rotation(rate=-0.1, about='phi')
        self.wait(gap)
        self.begin_ambient_camera_rotation(rate=0.1, about='theta')
        self.wait(gap)
        self.begin_ambient_camera_rotation(rate=0.1, about='gamma')
        self.wait(gap)
        self.stop_ambient_camera_rotation()
        self.wait()


class DashTest(Scene):
    def construct(self):
        def dash_updater(mob):
            offset = vt.get_value()
            mob['dashes'].become(mob.dash_objects(num_dashes, dash_ratio=0.5, offset=offset))

        plane = NumberPlane(
            background_line_style={
                "stroke_color": "#C2C2C2",
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        )
        mob1 = CubicBezier(3 * LEFT, UP, DOWN, 3 * RIGHT)
        vt = ValueTracker(0)
        num_dashes = 8
        speed = 7

        dash1 = DashedMObject(mob1, num_dashes=num_dashes, dashed_ratio=0.5, dash_offset=0)
        dash1.add_updater(dash_updater)

        self.add(plane, dash1)
        self.play(vt.animate.set_value(speed), run_time=6)
        self.wait()


class MatrixMultiplication(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        shapes = [(7, 8), (8, 5), (7, 5)]
        matrix1, matrix2, matrix3 = [WeightMatrix(shape=shape).set(width=0.4 * shape[1]) for shape in shapes]
        eq = Tex('=')

        for entry in matrix3.get_entries():
            entry.set_opacity(0)
        all_matrix = VGroup(matrix1, matrix2, eq, matrix3).arrange(RIGHT, buff=0.2)
        self.add(matrix1, matrix2, eq, matrix3)

        for i, row in enumerate(matrix1.get_rows()):
            for j, col in enumerate(matrix2.get_columns()):
                row_rect = SurroundingRectangle(row, color=BLUE, corner_radius=0.1).set_stroke(width=0.7)
                col_rect = SurroundingRectangle(col, color=BLUE, corner_radius=0.1).set_stroke(width=0.7)
                mul = VGroup(VGroup(row_rect, row),
                             VGroup(col_rect, col))
                mul_copy = mul.copy().arrange(RIGHT, buff=0.5).next_to(all_matrix, UP).scale(0.5)
                row3 = matrix3.get_rows()[i]
                entry = row3[j]

                self.play(TransformFromCopy(mul, mul_copy))
                self.play(FadeOut(mul_copy, target_position=entry.get_center()),
                          entry.animate.set_opacity(1))


class Tmp(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        gear = SVGMobject("assets/wheel.svg")
        gears_clip = VGroup(gear.copy().scale(0.5).shift(0.8 * UP).rotate(10 * DEGREES).set_color('#3fc1c9'),
                            gear.copy().scale(0.5).shift(0.55 * RIGHT).rotate(-8 * DEGREES).set_color('#364f6b'))
        text_clip = Text("CLIP Model", font_size=24, color=GREY).next_to(gears_clip, DOWN, SMALL_BUFF)
        surrounding_clip = SurroundingRectangle(VGroup(gears_clip, text_clip),
                                                buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        model_clip = VGroup(gears_clip, text_clip, surrounding_clip).move_to(4 * LEFT)

        gears = VGroup(gear.copy().scale(0.5).shift(0.78 * UP).set_color(YELLOW),
                       gear.copy().scale(0.5).shift(0.565 * LEFT).set_color(ORANGE),
                       gear.copy().scale(0.5).shift(0.57 * RIGHT))
        text_model = Text("Diffusion Model", font_size=24, color=GREY).next_to(gears, DOWN, SMALL_BUFF)
        surrounding_model = SurroundingRectangle(VGroup(gears, text_model),
                                                 buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        model_diffusion = VGroup(gears, text_model, surrounding_model)
        self.add(model_clip, model_diffusion)

        self.play(LaggedStart(
            AnimationGroup(
                Rotate(gears[i], axis=IN if i == 0 else OUT, about_point=gears[i].get_center())
                for i in range(3)
            ), run_time=4, lag_ratio=0.0))

        self.play(LaggedStart(
            AnimationGroup(
                Rotate(gears_clip[i], axis=IN if i == 0 else OUT, about_point=gears_clip[i].get_center())
                for i in range(2)
            ), run_time=4, lag_ratio=0.0))


class CurvedArrows(Scene):
    def construct(self):
        # 创建一个弯曲的箭头
        curved_arrow = CurvedArrow(start_point=LEFT, end_point=RIGHT, angle=PI / 2, color=BLUE)

        # 在场景中添加弯曲箭头
        self.play(Create(curved_arrow))
        self.wait()


if __name__ == "__main__":
    scene = TwoAndThreeDimensionalScene()
    scene.render()
