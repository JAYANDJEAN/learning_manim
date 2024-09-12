from helpers import *


class CountMatrixParameters(Scene):
    count_font_size = 36

    def construct(self):
        shape_list = [[(7, 7), (7, 6), (7, 6)],
                      [(8, 6), (6, 6), (8, 6)],
                      [(8, 5), (5, 6), (8, 6)],
                      [(7, 7), (7, 6), (7, 6)],
                      [(8, 6), (6, 6), (8, 6)]]
        matrix_mul = []
        for i, shapes in enumerate(shape_list):
            matrix1, matrix2, matrix3 = [
                VGroup(WeightMatrix(shape=shape).set(width=0.5 * shape[1]),
                       WeightMatrix(shape=shape).set(width=0.5 * shape[1])
                       .set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP),
                       WeightMatrix(shape=shape).set(width=0.5 * shape[1])
                       .set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP)
                       ) for shape in shapes]
            eq = Tex('=')
            mul = Tex('*')
            all_matrix = VGroup(matrix1, mul, matrix2, eq, matrix3).arrange(RIGHT, buff=0.5)

            self.play(LaggedStartMap(FadeIn, VGroup(matrix1, mul, matrix2, eq), lag_ratio=0.1))
            self.play(
                RandomizeMatrixEntries(matrix3[0]),
                LaggedStartMap(FadeIn, VGroup(matrix3[1], matrix3[2]), lag_ratio=0.1),
            )
            self.wait()
            self.play(FadeOut(all_matrix))


if __name__ == "__main__":
    scene = CountMatrixParameters()
    scene.render()
