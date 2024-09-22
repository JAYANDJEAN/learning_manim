from utils import *


# class RotateCamera(ThreeDCamera):
#     def construct(self):
#         self.set_floor_plane("xz")
#         self.play(frame.animate.reorient(-47, -7, 0, (-2.48, -5.84, -1.09), 20))
#         self.wait()


class RotateCameraExample(ThreeDScene):
    def construct(self):
        # image_prompt = ImageMobject("assets/prompt.png").set(height=4)
        # rect = SurroundingRectangle(image_prompt, buff=0.0)
        # image = Group(image_prompt, rect)
        # 是image太大了，所以效果不好
        lattice = NumberPlane(
            x_range=(-14, 14, 1),
            y_range=(-17, 17, 1),
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 1.0,
            },
            axis_config={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "include_numbers": False,
            },
            faded_line_ratio=0,
        ).set(width=4.0)
        angle_text = always_redraw(
            lambda: Text(
                f"phi: {self.camera.get_phi() / PI * 180:.2f}, theta: {self.camera.get_theta() / PI * 180:.2f}, gamma: {self.camera.get_gamma() / PI * 180:.2f}",
                font_size=12).to_edge(UP + LEFT)
        )
        self.add_fixed_in_frame_mobjects(angle_text)

        self.add(lattice)
        self.move_camera(phi=15 * DEGREES, run_time=3)
        self.wait()
        self.move_camera(theta=-45 * DEGREES, run_time=3)
        self.wait()
        self.move_camera(gamma=30 * DEGREES, run_time=3)


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
        gear = SVGMobject("assets/wheel.svg")
        gears = VGroup(gear.copy().scale(0.5).shift(0.78 * UP).set_color(YELLOW),
                       gear.copy().scale(0.5).shift(0.57 * LEFT).set_color(ORANGE),
                       gear.copy().scale(0.5).shift(0.57 * RIGHT))
        text_model = Text("Diffusion Model", font_size=24, color=GREY).next_to(gears, DOWN, SMALL_BUFF)
        surrounding_model = SurroundingRectangle(VGroup(gears, text_model),
                                                 buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        model_diffusion = VGroup(gears, text_model, surrounding_model)

        curve = VMobject()
        curve.start_new_path(model_diffusion.get_right())
        curve.add_cubic_bezier_curve_to(
            model_diffusion.get_right() + 3 * RIGHT + 3.0 * UP,
            model_diffusion.get_left() + 3 * LEFT + 3.0 * UP,
            model_diffusion.get_left()
        )
        curve.insert_n_curves(10).set_stroke(width=1.5).set_color(WHITE)

        # 定义四个控制点
        start = LEFT
        control1 = UP + LEFT * 2
        control2 = DOWN + RIGHT * 2
        end = RIGHT

        # 创建贝塞尔曲线
        bezier_curve = CubicBezier(start, control1, control2, end)

        # 添加贝塞尔曲线到场景
        self.add(bezier_curve)

        # 创建一个箭头并放在贝塞尔曲线的终点
        arrow_tip = ArrowTip().move_to(end)

        # 计算箭头的旋转角度，使其沿着曲线的方向
        direction = bezier_curve.point_from_proportion(1) - bezier_curve.point_from_proportion(0.99)
        arrow_tip.rotate(angle_of_vector(direction))

        self.add(model_diffusion, arrow_tip)
        # for n in range(4):
        #     self.play(
        #         ShowPassingFlash(curve, time_width=1.5, run_time=4),
        #         LaggedStart(
        #             AnimationGroup(
        #                 Rotate(gears[i],
        #                        axis=IN if i == 0 else OUT,
        #                        about_point=gears[i].get_center()
        #                        )
        #                 for i in range(3)
        #             ), lag_ratio=0.0, run_time=4)
        #     )
        # vt = ValueTracker(0)
        # num_dashes = 50
        # speed = 7
        #
        # dash1 = DashedMObject(curve, num_dashes=num_dashes, dashed_ratio=0.5, dash_offset=0)
        # dash1.add_updater(dash_updater)
        #
        # self.add(model_diffusion, dash1)
        # self.play(
        #     vt.animate.set_value(speed),
        #     LaggedStart(
        #         AnimationGroup(
        #             Rotate(gears[i],
        #                    axis=IN if i == 0 else OUT,
        #                    about_point=gears[i].get_center()
        #                    )
        #             for i in range(3)
        #         ), lag_ratio=0.0)
        #     , run_time=5, rate_func=linear
        # )
        # self.wait()


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


class RotateImageAroundYAxis(ThreeDScene):
    def construct(self):
        table_text = Rectangle(width=4.0, height=1.0, grid_xstep=1.0).move_to(3 * UP + 1 * LEFT)
        print(table_text.width, table_text.height)
        sour = SurroundingRectangle(table_text, buff=0.1)
        top = Dot(table_text.get_top())
        left = Dot(table_text.get_left())
        self.add(table_text, sour, top, left)


# 渲染场景
if __name__ == "__main__":
    path_cats = ([f"cat_with_noise/cat_{i:03}.jpg" for i in range(0, 150, 10)])
    print(path_cats)
    print(len(path_cats))
