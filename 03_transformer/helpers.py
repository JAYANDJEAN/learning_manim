from manim import *
import numpy as np
import os
from pathlib import Path
import warnings
from datasets import load_from_disk
import random
from typing import Optional,Tuple

# from manim.utils.color import Color  # Import the Color class

DATA_DIR = Path("output", "2024/transformers/data/")
WORD_FILE = Path(DATA_DIR, "OWL3_Dictionary.txt")


def get_paragraph(words, line_len=40, font_size=48):
    """
    Handle word wrapping
    """
    words = list(map(str.strip, words))
    word_lens = list(map(len, words))
    lines = []
    lh, rh = 0, 0
    while rh < len(words):
        rh += 1
        if sum(word_lens[lh:rh]) > line_len:
            rh -= 1
            lines.append(words[lh:rh])
            lh = rh
    lines.append(words[lh:])
    text = "\n".join([" ".join(line).strip() for line in lines])
    return Text(text, font_size=font_size, line_spacing=1.2).set_align("LEFT")


# No manim
def softmax(logits, temperature=1.0):
    logits = np.array(logits)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')  # Ignore all warnings within this block
        logits = logits - np.max(logits)  # For numerical stability
        exps = np.exp(np.divide(logits, temperature, where=temperature != 0))

    if np.isinf(exps).any() or np.isnan(exps).any() or temperature == 0:
        result = np.zeros_like(logits)
        result[np.argmax(logits)] = 1
        return result
    return exps / np.sum(exps)


# manim color
def value_to_color(value, low_positive_color=BLUE_E, high_positive_color=BLUE_B,
                   low_negative_color=RED_E, high_negative_color=RED_B,
                   min_value=0.0, max_value=10.0):
    alpha = np.clip(float((value - min_value) / (max_value - min_value)), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color(*colors, alpha)


def read_in_book(name="tale_of_two_cities"):
    return Path(DATA_DIR, name).with_suffix(".txt").read_text()


# no manim
def load_image_net_data(dataset_name="image_net_1k"):
    data_path = Path(Path.home(), "Documents", dataset_name)
    image_dir = Path(data_path, "images")
    label_category_path = Path(DATA_DIR, "image_categories.txt")
    image_label_path = Path(data_path, "image_labels.txt")

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        image_data = load_from_disk(str(data_path))
        indices = range(len(image_data))
        categories = label_category_path.read_text().split("\n")
        labels = [categories[image_data[index]['label']] for index in indices]
        image_label_path.write_text("\n".join(labels))
        for index in indices:
            image = image_data[index]['image']
            image.save(str(Path(image_dir, f"{index}.jpeg")))

    labels = image_label_path.read_text().split("\n")
    return [
        (Path(image_dir, f"{index}.jpeg"), label)
        for index, label in enumerate(labels)
    ]


def show_matrix_vector_product(scene, matrix, vector, buff=0.25, x_max=999):
    # Show product
    eq = MathTex("=")
    eq.set_width(0.5 * vector.width)
    # shape = (matrix.shape[0], 1)
    rhs = DecimalNumber(
        number=x_max,
        show_ellipsis=True,
        include_sign=True,
    )
    rhs.scale(vector.height / rhs.height)
    eq.next_to(vector, RIGHT, buff=buff)
    rhs.next_to(eq, RIGHT, buff=buff)

    scene.play(FadeIn(eq), FadeIn(rhs))

    last_rects = VGroup()
    n_rows = len(matrix)
    for n, row in enumerate(matrix):
        if n == (len(matrix) // 2):  # Assuming ellipses row is the middle one
            scene.add(rhs)
        else:
            rects = scene.add_highlighted_rects_to_vector(row, vector)
            last_rects.add(rects)
    scene.play(FadeOut(last_rects))

    return eq, rhs


class MatrixVectorScene(Scene):
    def construct(self):
        matrix = np.array([[1, 2], [3, 4], [5, 6]])
        vector = np.array([[7], [8]])
        matrix_mob = Matrix(matrix)
        vector_mob = Matrix(vector)
        matrix_mob.next_to(ORIGIN, LEFT)
        vector_mob.next_to(matrix_mob, RIGHT)

        self.add(matrix_mob, vector_mob)
        eq, rhs = show_matrix_vector_product(self, matrix_mob, vector_mob)
        self.wait(2)


def matrix_row_vector_product(scene, row, vector, entry, to_fade):
    def get_rect(elem):
        return SurroundingRectangle(elem, buff=0.1).set_stroke(YELLOW, 2)

    row_rects = VGroup(*map(get_rect, row))
    vect_rects = VGroup(*map(get_rect, vector[:len(row)]))
    partial_values = [0]
    for e1, e2 in zip(row, vector[:len(row)]):
        if isinstance(e1, DecimalNumber) and isinstance(e2, DecimalNumber):
            increment = e1.get_value() * e2.get_value()
        else:
            increment = 0
        partial_values.append(partial_values[-1] + increment)
    n_values = len(partial_values)

    scene.play(
        ShowIncreasingSubsets(row_rects),
        ShowIncreasingSubsets(vect_rects),
        UpdateFromAlphaFunc(entry, lambda m, a: m.set_value(
            partial_values[min(int(np.round(a * (n_values - 1))), n_values - 1)]
        )),
        FadeOut(to_fade),
        rate_func=linear,
    )

    return VGroup(row_rects, vect_rects)


def get_full_matrix_vector_product(
        mat_sym="w",
        vect_sym="x",
        n_rows=5,
        n_cols=5,
        mat_sym_color=BLUE,
        height=3.0,
        ellipses_row=-2,
        ellipses_col=-2,
):
    m_indices = list(map(str, range(1, n_cols + 1)))
    n_indices = list(map(str, range(1, n_rows + 1)))
    matrix = Matrix(
        [
            [Rf"{mat_sym}_{{{m}, {n}}}" for n in n_indices]
            for m in m_indices
        ],
    )
    matrix.set_height(height)
    matrix.get_entries().set_color(mat_sym_color)
    vector = Matrix(
        [[Rf"{vect_sym}_{{{n}}}"] for n in n_indices],
    )
    vector.match_height(matrix)
    vector.next_to(matrix, RIGHT)
    equals = MathTex("=")
    equals.next_to(vector, RIGHT)

    result_terms = [
        [Rf"{mat_sym}_{{{m}, {n}}} {vect_sym}_{{{n}}}" for n in n_indices]
        for m in m_indices
    ]
    rhs = Matrix(
        result_terms,
    )
    rhs.match_height(matrix)
    rhs.next_to(equals, RIGHT)
    for m, row in enumerate(rhs.get_rows()):
        for n, entry in enumerate(row):
            entry.set_color_by_tex(f"{mat_sym}_", mat_sym_color)
        for e1, e2 in zip(row, row[1:]):
            plus = MathTex("+")
            plus.match_height(e1)
            plus.next_to(e1, RIGHT, SMALL_BUFF)
            e2.shift(RIGHT * plus.get_width())
            e2.add(plus)

    return matrix, vector, equals, rhs


def show_symbolic_matrix_vector_product(scene, matrix, vector, rhs, run_time_per_row=0.75):
    last_rects = VGroup()
    for mat_row, rhs_row in zip(matrix.get_rows(), rhs.get_rows()):
        mat_rects = VGroup(*map(SurroundingRectangle, mat_row))
        vect_rects = VGroup(*map(SurroundingRectangle, vector.get_columns()[0]))
        rect_group = VGroup(mat_rects, vect_rects)
        rect_group.set_stroke(YELLOW, 2)
        scene.play(
            FadeOut(last_rects),
            ShowIncreasingSubsets(mat_rects, run_time=run_time_per_row),
            ShowIncreasingSubsets(vect_rects, run_time=run_time_per_row),
            ShowIncreasingSubsets(rhs_row, run_time=run_time_per_row),
        )
        last_rects = rect_group
    scene.play(FadeOut(last_rects))


def data_flying_animation(point, vect=2 * DOWN + RIGHT, color=GREY_C, max_opacity=0.75):
    word = Text("Data", color=color)
    return UpdateFromAlphaFunc(
        word, lambda m, a: m.move_to(
            interpolate(point, point + vect, a)
        ).set_opacity(there_and_back(a) * max_opacity)
    )


def get_data_modifying_matrix_anims(matrix, word_shape=(5, 10), alpha_maxes=(0.7, 0.9), shift_vect=2 * DOWN + RIGHT,
                                    run_time=3):
    x_min, x_max = [matrix.get_left()[0], matrix.get_right()[0]]
    y_min, y_max = [matrix.get_bottom()[1], matrix.get_top()[1]]
    z = matrix.get_center()[2]
    points = np.array([
        [
            interpolate(x_min, x_max, a1),
            interpolate(y_min, y_max, a2),
            z,
        ]
        for a1 in np.linspace(0, alpha_maxes[1], word_shape[1])
        for a2 in np.linspace(0, alpha_maxes[0], word_shape[0])
    ])
    return [
        LaggedStart(
            *[
                data_flying_animation(p, vect=shift_vect)
                for p in points
            ],
            lag_ratio=1 / len(points),
            run_time=run_time
        ),
        ApplyWave(matrix, run_time=run_time),
    ]


def data_modifying_matrix(scene, matrix, *args, **kwargs):
    anims = get_data_modifying_matrix_anims(matrix, *args, **kwargs)
    scene.play(*anims)


def create_pixels(image_mob, pixel_width=0.1):
    x0, y0, _ = image_mob.get_corner(UL)
    x1, y1, _ = image_mob.get_corner(DR)
    points = np.array([
        [x, y, 0]
        for y in np.arange(y0, y1, -pixel_width)
        for x in np.arange(x0, x1, pixel_width)
    ])
    square = Square(pixel_width).set_fill(WHITE, 1).set_stroke(width=0)
    pixels = VGroup(
        # *[
        #     square.copy().move_to(point, UL).set_color(
        #         Color(rgb=image_mob.point_to_rgb(point))
        #     )
        #     for point in points
        # ]
    )
    return pixels


class NeuralNetwork(VGroup):
    def __init__(
            self,
            layer_sizes=[6, 12, 6],
            neuron_radius=0.1,
            v_buff_ratio=1.0,
            h_buff_ratio=7.0,
            max_stroke_width=2.0,
            stroke_decay=2.0,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.max_stroke_width = max_stroke_width
        self.stroke_decay = stroke_decay

        layers = VGroup(*[
            VGroup(*[Dot(radius=neuron_radius) for _ in range(size)])
            for size in layer_sizes
        ])
        layers.arrange(RIGHT, buff=h_buff_ratio)
        layers.center()

        for layer in layers:
            layer.arrange(DOWN, buff=v_buff_ratio)

        lines = VGroup(*[
            VGroup(*[
                Line(start=n1.get_center(), end=n2.get_center())
                for n1 in l1 for n2 in l2
            ])
            for l1, l2 in zip(layers[:-1], layers[1:])
        ])

        self.add(layers, lines)
        self.layers = layers
        self.lines = lines

        self.randomize_layer_values()
        self.randomize_line_style()

    def randomize_layer_values(self):
        for group in self.lines:
            for line in group:
                line.set_stroke(
                    color=value_to_color(random.uniform(-10, 10)),
                    width=self.max_stroke_width * random.random() ** self.stroke_decay,
                )
        return self

    def randomize_line_style(self):
        for layer in self.layers:
            for dot in layer:
                dot.set_stroke(WHITE, 1)
                dot.set_fill(WHITE, opacity=random.random())
        return self


class ContextAnimation(LaggedStart):
    def __init__(
            self,
            target,
            sources,
            direction=UP,
            hue_range=(0.1, 0.3),
            time_width=2,
            min_stroke_width=0,
            max_stroke_width=5,
            lag_ratio=None,
            strengths=None,
            run_time=3,
            fix_in_frame=False,
            path_arc=PI / 2,
            **kwargs,
    ):
        arcs = VGroup()
        if strengths is None:
            strengths = np.random.random(len(sources)) ** 2

        for source, strength in zip(sources, strengths):
            sign = direction[1] * (-1) ** int(source.get_x() < target.get_x())
            arc = ArcBetweenPoints(
                source.get_edge_center(direction),
                target.get_edge_center(direction),
                angle=sign * path_arc,
                stroke_color=random_bright_color(hue_range=hue_range),
                stroke_width=interpolate(
                    min_stroke_width,
                    max_stroke_width,
                    strength,
                )
            )
            arcs.add(arc)

        if fix_in_frame:
            arcs.fix_in_frame()
        arcs.shuffle()
        lag_ratio = 0.5 / len(arcs) if lag_ratio is None else lag_ratio

        super().__init__(
            *[VShowPassingFlash(arc, time_width=time_width) for arc in arcs],
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )


class Vect3:
    pass


class LabeledArrow(Arrow):
    def __init__(
            self,
            *args,
            label_text: Optional[str] = None,
            font_size: float = 24,
            label_buff: float = 0.1,
            direction: Optional[Vect3] = None,
            label_rotation: float = PI / 2,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        if label_text is not None:
            start, end = self.get_start_and_end()
            label = Text(label_text, font_size=font_size)
            label.set_fill(self.get_color())
            label.rotate(label_rotation)
            if direction is None:
                direction = normalize(end - start)
            label.next_to(end, direction, buff=label_buff)
            self.add(label)


class WeightMatrix(DecimalMatrix):
    def __init__(
            self,
            values: Optional[np.ndarray] = None,
            shape: tuple[int, int] = (6, 8),
            value_range: tuple[float, float] = (-9.9, 9.9),
            ellipses_row: Optional[int] = -2,
            ellipses_col: Optional[int] = -2,
            num_decimal_places: int = 1,
            bracket_h_buff: float = 0.1,
            decimal_config=dict(include_sign=True),
            low_positive_color: ManimColor = BLUE_E,
            high_positive_color: ManimColor = BLUE_B,
            low_negative_color: ManimColor = RED_E,
            high_negative_color: ManimColor = RED_B,
            **kwargs,
    ):
        if values is None:
            values = np.random.uniform(*value_range, size=shape)

        super().__init__(
            values=values,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=decimal_config,
            ellipses_row=ellipses_row,
            ellipses_col=ellipses_col,
            **kwargs,
        )

        self.low_positive_color = low_positive_color
        self.high_positive_color = high_positive_color
        self.low_negative_color = low_negative_color
        self.high_negative_color = high_negative_color
        self.reset_entry_colors()

    def reset_entry_colors(self):
        for entry in self.get_entries():
            entry.set_fill(
                value_to_color(
                    entry.get_value(),
                    self.low_positive_color,
                    self.high_positive_color,
                    self.low_negative_color,
                    self.high_negative_color,
                    0, max(self.value_range),
                )
            )
        return self


class NumericEmbedding(WeightMatrix):
    def __init__(
            self,
            values: Optional[np.ndarray] = None,
            shape: Optional[Tuple[int, int]] = None,
            length: int = 7,
            num_decimal_places: int = 1,
            ellipses_row: int = -2,
            ellipses_col: int = -2,
            value_range: tuple[float, float] = (-9.9, 9.9),
            bracket_h_buff: float = 0.1,
            decimal_config=dict(include_sign=True),
            dark_color: ManimColor = GREY_C,
            light_color: ManimColor = WHITE,
            **kwargs,
    ):
        if values is not None:
            if len(values.shape) == 1:
                values = values.reshape((values.shape[0], 1))
            shape = values.shape
        if shape is None:
            shape = (length, 1)
        super().__init__(
            values,
            shape=shape,
            value_range=value_range,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=decimal_config,
            low_positive_color=dark_color,
            high_positive_color=light_color,
            low_negative_color=dark_color,
            high_negative_color=light_color,
            ellipses_row=ellipses_row,
            ellipses_col=ellipses_col,
            **kwargs,
        )


class RandomizeMatrixEntries(Animation):
    def __init__(self, matrix, **kwargs):
        self.matrix = matrix
        self.entries = matrix.get_entries()
        self.start_values = [entry.get_value() for entry in self.entries]
        self.target_values = np.random.uniform(
            matrix.value_range[0],
            matrix.value_range[1],
            len(self.entries)
        )
        super().__init__(matrix, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        for index, entry in enumerate(self.entries):
            start = self.start_values[index]
            target = self.target_values[index]
            sub_alpha = self.get_sub_alpha(alpha, index, len(self.entries))
            entry.set_value(interpolate(start, target, sub_alpha))
        self.matrix.reset_entry_colors()


class EmbeddingSequence(MobjectMatrix):
    pass


class AbstractEmbeddingSequence(MobjectMatrix):
    pass


class VShowPassingFlash:
    pass


class Dial(VGroup):
    def __init__(
            self,
            radius=0.5,
            relative_tick_size=0.2,
            value_range=(0, 1, 0.1),
            initial_value=0,
            arc_angle=270 * DEGREES,
            stroke_width=2,
            stroke_color=WHITE,
            needle_color=BLUE,
            needle_stroke_width=5.0,
            value_to_color_config=dict(),
            set_anim_streak_color=TEAL,
            set_anim_streak_width=4,
            set_value_anim_streak_density=6,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.value_range = value_range
        self.value_to_color_config = value_to_color_config
        self.set_anim_streak_color = set_anim_streak_color
        self.set_anim_streak_width = set_anim_streak_width
        self.set_value_anim_streak_density = set_value_anim_streak_density

        # Main dial
        self.arc = Arc(arc_angle / 2, -arc_angle, radius=radius)
        self.arc.rotate(90 * DEGREES, about_point=ORIGIN)

        low, high, step = value_range
        n_values = int(1 + (high - low) / step)
        tick_points = map(self.arc.pfp, np.linspace(0, 1, n_values))
        self.ticks = VGroup(*(
            Line((1.0 - relative_tick_size) * point, point)
            for point in tick_points
        ))
        self.bottom_point = VectorizedPoint(radius * DOWN)
        for mob in self.arc, self.ticks:
            mob.set_stroke(stroke_color, stroke_width)

        self.add(self.arc, self.ticks, self.bottom_point)

        # Needle
        self.needle = Line()
        self.needle.set_stroke(
            color=needle_color,
            width=[needle_stroke_width, 0]
        )
        self.add(self.needle)

        # Initialize
        self.set_value(initial_value)

    def value_to_point(self, value):
        low, high, step = self.value_range
        alpha = inverse_interpolate(low, high, value)
        return self.arc.pfp(alpha)

    def set_value(self, value):
        self.needle.put_start_and_end_on(
            self.get_center(),
            self.value_to_point(value)
        )
        self.needle.set_color(value_to_color(
            value,
            min_value=self.value_range[0],
            max_value=self.value_range[1],
            **self.value_to_color_config
        ))

    def animate_set_value(self, value, **kwargs):
        kwargs.pop("path_arc", None)
        center = self.get_center()
        points = [self.needle.get_end(), self.value_to_point(value)]
        vects = [point - center for point in points]
        angle1, angle2 = [
            (angle_of_vector(vect) + TAU / 4) % TAU - TAU / 4
            for vect in vects
        ]
        path_arc = angle2 - angle1

        density = self.set_value_anim_streak_density
        radii = np.linspace(0, 0.5 * self.get_width(), density + 1)[1:]
        diff_arcs = VGroup(*(
            Arc(
                angle1, angle2 - angle1,
                radius=radius,
                arc_center=center,
            )
            for radius in radii
        ))
        diff_arcs.set_stroke(self.set_anim_streak_color, self.set_anim_streak_width)

        return AnimationGroup(
            self.animate.set_value(value).set_anim_args(path_arc=path_arc, **kwargs),
            *(
                VShowPassingFlash(diff_arc, time_width=1.5, **kwargs)
                for diff_arc in diff_arcs
            )
        )

    def get_random_value(self):
        low, high, step = self.value_range
        return interpolate(low, high, random.random())


class MachineWithDials(VGroup):
    default_dial_config = dict(
        stroke_width=1.0,
        needle_stroke_width=5.0,
        relative_tick_size=0.25,
        set_anim_streak_width=2,
    )

    def __init__(
            self,
            width=5.0,
            height=4.0,
            n_rows=6,
            n_cols=8,
            dial_buff_ratio=0.5,
            stroke_color=WHITE,
            stroke_width=1,
            fill_color=GREY_D,
            fill_opacity=1.0,
            dial_config=dict(),
    ):
        super().__init__()
        box = Rectangle(width, height)
        box.set_stroke(stroke_color, stroke_width)
        box.set_fill(fill_color, fill_opacity)
        self.box = box

        dial_config = dict(**self.default_dial_config, **dial_config)
        dials = Dial(**dial_config).get_grid(n_rows, n_cols, buff_ratio=dial_buff_ratio)
        buff = dials[0].get_width() * dial_buff_ratio
        dials.set_width(box.get_width() - buff)
        dials.set_max_height(box.get_width() - buff)
        dials.move_to(box)
        for dial in dials:
            dial.set_value(dial.get_random_value())
        self.dials = dials

        self.add(box, dials)

    def random_change_animation(self, lag_factor=0.5, run_time=3.0, **kwargs):
        return LaggedStart(
            *(
                dial.animate_set_value(dial.get_random_value())
                for dial in self.dials
            ), lag_ratio=lag_factor / len(self.dials),
            run_time=run_time,
            **kwargs
        )

    def rotate_all_dials(self, run_time=2, lag_factor=1.0):
        shuffled_dials = list(self.dials)
        random.shuffle(shuffled_dials)
        return LaggedStart(
            *(
                Rotate(dial.needle, TAU, about_point=dial.get_center())
                for dial in shuffled_dials
            ),
            lag_ratio=lag_factor / len(self.dials)
        )
