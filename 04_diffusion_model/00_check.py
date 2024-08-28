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
        matrix1 = WeightMatrix(shape=(7, 8)).set(width=4.8)
        matrix2 = WeightMatrix(shape=(8, 5)).set(width=3.0)
        eq = Tex('=')
        matrix3 = WeightMatrix(shape=(7, 5)).set(width=3.0)
        VGroup(matrix1, matrix2, eq, matrix3).arrange(RIGHT, buff=0.2)
        self.add(matrix1, matrix2, eq, matrix3)



if __name__ == "__main__":
    scene = MatrixMultiplication()
    scene.render()
