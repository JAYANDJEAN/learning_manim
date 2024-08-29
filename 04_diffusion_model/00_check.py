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
        mob1 = CubicBezier(3 * LEFT, UP, DOWN, 3 * RIGHT)
        vt = ValueTracker(0)
        num_dashes = 8
        speed = 7

        dash1 = DashedMObject(mob1, num_dashes=num_dashes, dashed_ratio=0.5, dash_offset=0)
        dash1.add_updater(dash_updater)

        self.add(plane, dash1)
        self.play(vt.animate.set_value(speed), run_time=6)
        self.wait()


class ImageShow(Scene):
    def construct(self):
        matrix1 = WeightMatrix(shape=(12, 7)).set(width=4)
        matrix2 = WeightMatrix(shape=(12, 7)).set(width=4).set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP)
        matrix3 = WeightMatrix(shape=(12, 7)).set(width=4).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP)
        self.add(matrix3, matrix2, matrix1)


class MatrixMultiplication(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        shapes = [(7, 8), (8, 5), (7, 5)]
        matrix1, matrix2, matrix3 = [WeightMatrix(shape=shape).set(width=0.5 * shape[1]) for shape in shapes]
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
    scene = MatrixMultiplication()
    scene.render()
