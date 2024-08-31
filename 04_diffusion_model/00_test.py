from utils import *


class RotateCameraExample(ThreeDScene):
    def construct(self):
        image_prompt = ImageMobject("assets/prompt.png")

        # 设置初始视角
        images = Group(
            ImageMobject("assets/prompt_b.png"),
            ImageMobject("assets/prompt_g.png"),
            ImageMobject("assets/prompt_r.png"),
            ImageMobject("assets/prompt.png"), ).set(height=5).arrange(OUT, buff=1)
        self.add(images)
        self.move_camera(phi=-50 * DEGREES,
                         theta=-140 * DEGREES,
                         gamma=-37 * DEGREES,
                         focal_distance=30,
                         frame_center=LEFT + DOWN * 0.3)

        self.set_camera_orientation(phi=-50 * DEGREES,
                                    theta=-140 * DEGREES,
                                    gamma=-37 * DEGREES,
                                    focal_distance=30,
                                    frame_center=LEFT + DOWN * 0.3)


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


if __name__ == "__main__":
    scene = RotateCameraExample()
    scene.render()
