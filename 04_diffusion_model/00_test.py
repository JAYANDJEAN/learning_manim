from utils import *


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
        for n in range(4):
            self.play(
                ShowPassingFlash(curve, time_width=1.5, run_time=4),
                LaggedStart(
                    AnimationGroup(
                        Rotate(gears[i],
                               axis=IN if i == 0 else OUT,
                               about_point=gears[i].get_center()
                               )
                        for i in range(3)
                    ), lag_ratio=0.0, run_time=4)
            )
        vt = ValueTracker(0)
        num_dashes = 50
        speed = 7

        dash1 = DashedMObject(curve, num_dashes=num_dashes, dashed_ratio=0.5, dash_offset=0)
        dash1.add_updater(dash_updater)

        self.add(model_diffusion, dash1)
        self.play(
            vt.animate.set_value(speed),
            LaggedStart(
                AnimationGroup(
                    Rotate(gears[i],
                           axis=IN if i == 0 else OUT,
                           about_point=gears[i].get_center()
                           )
                    for i in range(3)
                ), lag_ratio=0.0)
            , run_time=5, rate_func=linear
        )
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


class PrismGroup(Diffusion):
    def construct(self):
        self.add(self.unet)
        self.play(
            LaggedStart(
                *[p.animate(rate_func=there_and_back).set_color(TEAL)
                  for prism in self.unet[0] for p in prism],
                lag_ratio=0.1, run_time=1.5
            )
        )
        self.wait()


if __name__ == "__main__":
    PrismGroup().render()
