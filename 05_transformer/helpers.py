from typing import Optional, Tuple

from manim import *


def bake_mobject_into_vector_entries(mob, vector, path_arc=30 * DEGREES, group_type=None):
    entries = vector.get_entries()
    mob_copies = Group(*(mob.copy() for _ in range(len(entries))))
    return AnimationGroup(
        LaggedStart(
            (FadeOut(mc, target_position=entry.get_center(), path_arc=path_arc)
             for mc, entry in zip(mob_copies, entries)),
            lag_ratio=0.05,
            group_type=group_type,
            run_time=2,
            remover=True
        ),
        RandomizeMatrixEntries(
            vector,
            rate_func=lambda t: clip(smooth(2 * t - 1), 0, 1),
            run_time=2
        ),
    )


def value_to_color(value,
                   low_positive_color=BLUE_A,
                   high_positive_color=BLUE_E,
                   low_negative_color=RED_A,
                   high_negative_color=RED_E,
                   min_value=0.0,
                   max_value=10.0):
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color(*colors, alpha)


class WeightMatrix(DecimalMatrix):
    def __init__(self,
                 values: Optional[np.ndarray] = None,
                 shape: tuple[int, int] = (6, 8),
                 value_range: tuple[float, float] = (-9.9, 9.9)):

        if values is not None:
            shape = values.shape
        self.shape = shape
        self.value_range = value_range

        if values is None:
            values = np.random.uniform(*self.value_range, size=shape)

        super().__init__(values)
        self.reset_entry_colors()

    def reset_entry_colors(self):
        for entry in self.get_entries():
            entry.set_color(color=value_to_color(
                entry.get_value(), min_value=0, max_value=max(self.value_range))
            )
        return self


# todo: 没有省略号
class NumericEmbedding(WeightMatrix):
    def __init__(self,
                 values: Optional[np.ndarray] = None,
                 shape: Optional[Tuple[int, int]] = None,
                 length: int = 7,
                 value_range: tuple[float, float] = (-9.9, 9.9),
                 **kwargs,
                 ):

        if values is not None:
            if len(values.shape) == 1:
                values = values.reshape((values.shape[0], 1))
            shape = values.shape
        if shape is None:
            shape = (length, 1)
        super().__init__(values, shape=shape, value_range=value_range)


class RandomizeMatrixEntries(Animation):
    def __init__(self, matrix, **kwargs):
        self.matrix = matrix
        self.entries = matrix.get_entries()
        self.start_values = [entry.get_value() for entry in self.entries]
        # self.target_values = np.random.uniform(
        #     matrix.value_range[0],
        #     matrix.value_range[1],
        #     len(self.entries)
        # )
        # todo: 不完美
        self.target_values = [np.random.uniform(0, matrix.value_range[1]) if x > 0
                              else np.random.uniform(matrix.value_range[0], 0) for x in self.start_values]
        super().__init__(matrix, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        for index, entry in enumerate(self.entries):
            start = self.start_values[index]
            target = self.target_values[index]
            sub_alpha = self.get_sub_alpha(alpha, index, len(self.entries))
            entry.set_value(interpolate(start, target, sub_alpha))

        self.matrix.reset_entry_colors()
        # self.matrix.element_alignment_corner = DR


def matrix_row_vector_product(scene, row, vector, entry, to_fade):
    def get_rect(elem):
        return SurroundingRectangle(elem, buff=0.1).set_stroke(YELLOW, 2)

    row_rects = VGroup(*map(get_rect, row))
    vect_rects = VGroup(*map(get_rect, vector[:-2]))
    partial_values = [0]
    for e1, e2 in zip(row, vector[:-2]):
        if not isinstance(e1, DecimalNumber) and isinstance(e2, DecimalNumber):
            increment = 0
        else:
            val1 = round(e1.get_value(), e1.num_decimal_places)
            val2 = round(e2.get_value(), e2.num_decimal_places)
            increment = val1 * val2
        partial_values.append(partial_values[-1] + increment)
    n_values = len(partial_values)

    scene.play(
        ShowIncreasingSubsets(row_rects),
        ShowIncreasingSubsets(vect_rects),
        UpdateFromAlphaFunc(entry, lambda m, a: m.set_value(
            partial_values[min(int(np.round(a * n_values)), n_values - 1)]
        )),
        FadeOut(to_fade),
        rate_func=linear,
    )

    return VGroup(row_rects, vect_rects)


def show_matrix_vector_product(scene, matrix, vector, buff=0.25, x_max=999):
    # Show product
    eq = Tex("=")
    eq.set_width(0.5 * vector.get_width())
    shape = (matrix.shape[0], 1)
    rhs = NumericEmbedding(
        values=x_max * np.ones(shape),
        value_range=(-x_max, x_max)
    )
    rhs.scale(vector.elements[0].get_height() / rhs.elements[0].get_height())
    eq.next_to(vector, RIGHT, buff=buff)
    rhs.next_to(eq, RIGHT, buff=buff)

    scene.play(FadeIn(eq), FadeIn(rhs.get_brackets()))

    last_rects = VGroup()
    n_rows = len(matrix.get_entries())
    for n, row, entry in zip(range(n_rows), matrix.get_rows(), rhs[:-2]):
        last_rects = matrix_row_vector_product(scene, row, vector, entry, last_rects)
    scene.play(FadeOut(last_rects))

    return eq, rhs
