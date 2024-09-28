import random
from typing import Optional, Tuple

from manim import *


def bake_mobject_into_vector_entries(mob, vector, path_arc=30 * DEGREES, group_type=None):
    entries = vector.get_entries()
    mob_copies = Group(*(mob.copy() for _ in range(len(entries))))
    return AnimationGroup(
        LaggedStart(*[FadeOut(mc, target_position=entry.get_center(), path_arc=path_arc)
                      for mc, entry in zip(mob_copies, entries)],
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


def value_to_color(value, min_value=0.0, max_value=10.0):
    low_positive_color = BLUE_A
    high_positive_color = BLUE_E
    low_negative_color = RED_A
    high_negative_color = RED_E
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color(*colors, alpha)


class MultiLayerPerceptron(MovingCameraScene):
    def construct(self):
        def create_composed_shape(radius):
            circle = Circle(radius=radius, color=WHITE).set_stroke(width=1.5)
            line1 = Line(circle.get_center(), circle.point_at_angle(PI / 3), color=BLUE_B).set_stroke(width=2)
            line2 = Line(circle.get_center(), circle.point_at_angle(PI), color=BLUE_B).set_stroke(width=2)
            return VGroup(circle, line1, line2)

        def create_connections(nodes_in, nodes_out):
            full_connections = VGroup()
            combinations = [(x, y) for x in range(len(nodes_in)) for y in range(len(nodes_out))]
            random_choices = random.sample(combinations, 5)
            for i, node1 in enumerate(nodes_in):
                for j, node2 in enumerate(nodes_out):
                    if node2.get_color() != ORANGE:
                        line = Line(node1.get_right(), node2.get_left(), buff=SMALL_BUFF)
                        line.set_stroke(GREY_B, width=random.random() ** 2, opacity=random.random() ** 0.25)
                        if (i, j) in random_choices:
                            line.set_stroke(WHITE, width=0.5 + random.random(), opacity=1)
                        full_connections.add(line)
            return full_connections

        self.camera.background_color = "#1C1C1C"
        num_layers = 7
        random_integers = [random.randint(5, 7) for _ in range(num_layers)]
        dict_layer_nodes = dict()
        for i, num_nodes in enumerate(random_integers):
            if i == 0:
                circles = ([Circle(radius=0.2, color=ORANGE).set_stroke(width=1.5)] +
                           [Circle(radius=0.2, color=WHITE).set_stroke(width=1.5) for _ in range(num_nodes)])
            elif i == len(random_integers) - 1:
                circles = [Circle(radius=0.2, color=WHITE).set_stroke(width=1.5) for _ in range(num_nodes)]
            else:
                circles = ([Circle(radius=0.2, color=ORANGE).set_stroke(width=1.5)] +
                           [create_composed_shape(0.2) for _ in range(num_nodes)])
            dict_layer_nodes[i] = VGroup(*circles).arrange(UP, buff=0.3)

        node01 = VGroup(dict_layer_nodes[0], dict_layer_nodes[1]).arrange(RIGHT, buff=3)
        connections01 = create_connections(dict_layer_nodes[0], dict_layer_nodes[1])
        brace_in = Brace(node01[0], direction=LEFT)
        brace_in_text = Text("Input", font_size=24, color=YELLOW).next_to(brace_in, LEFT, SMALL_BUFF)
        brace_out = Brace(node01[1], direction=RIGHT)
        brace_out_text = Text("Output", font_size=24, color=YELLOW).next_to(brace_out, RIGHT, SMALL_BUFF)
        brace_01 = Brace(node01, direction=UP)
        brace_01_text = Text("Parameters", font_size=24, color=YELLOW).next_to(brace_01, UP, SMALL_BUFF)
        node01_copy = node01.copy()
        nodes = VGroup(*dict_layer_nodes.values()).arrange(RIGHT, buff=1.3)
        connections = VGroup(*[create_connections(dict_layer_nodes[i], dict_layer_nodes[i + 1])
                               for i in range(num_layers - 1)])
        brace_mlp = Brace(nodes, direction=UP)
        brace_mlp_text = Text("MultiLayerPerceptron", font_size=24, color=YELLOW).next_to(brace_mlp, UP, SMALL_BUFF)

        self.play(Create(node01_copy[0]))
        self.play(Create(brace_in))
        self.play(Create(brace_in_text))
        self.play(Create(node01_copy[1]))
        self.play(Create(brace_out))
        self.play(Create(brace_out_text))
        self.play(Create(connections01))
        self.play(Create(brace_01))
        self.play(Create(brace_01_text))
        self.play(FadeOut(brace_in, brace_in_text, brace_out, brace_out_text, brace_01, brace_01_text),
                  FadeOut(connections01))

        self.wait()
        self.play(Transform(node01_copy, nodes))
        self.wait()
        self.play(Create(connections))
        self.play(Create(brace_mlp), Create(brace_mlp_text))


class ArrowWithLabel(Arrow):
    def __init__(self,
                 *args,
                 label: Text | ImageMobject = None,
                 label_buff: float = 0.1,
                 label_rotation: float = PI / 2,
                 **kwargs
                 ):
        super().__init__(*args, **kwargs)
        self.label = label
        start, end = self.get_start_and_end()
        direction = normalize(end - start)
        self.label.rotate(label_rotation, RIGHT)
        self.label.next_to(end, direction, buff=label_buff)


class PathMapper(VMobject):
    def __init__(self, path_source: VMobject, num_of_path_points=100, **kwargs):
        super().__init__(**kwargs)
        self.num_of_path_points = num_of_path_points
        self.path = path_source
        self.generate_length_map()

    def generate_length_map(self):
        norms = np.array(0)
        for k in range(self.path.get_num_curves()):
            norms = np.append(norms, self.path.get_nth_curve_length_pieces(k, sample_points=11))
        # add up length-pieces in array form
        self.pathdata_lengths = np.cumsum(norms)
        self.pathdata_alpha = np.linspace(0, 1, self.pathdata_lengths.size)

    def cubic_to_quads(self, cubic_points):
        # based on https://ttnghia.github.io/pdf/QuadraticApproximation.pdf
        q_points = np.empty((0, 3))
        gamma = 0.5
        q1 = cubic_points[0, :] + 3 / 2 * gamma * (cubic_points[1, :] - cubic_points[0, :])
        q3 = cubic_points[3, :] + 3 / 2 * (1 - gamma) * (cubic_points[2, :] - cubic_points[3, :])
        q2 = (1 - gamma) * q1 + gamma * q3
        q0 = cubic_points[0, :]
        q4 = cubic_points[3, :]
        q_points = np.append(q_points, (q0, q1, q2, q2, q3, q4), axis=0)
        return q_points

    def calc_len_bezier_quad(self, points):
        a = points[0, :]
        b = points[1, :]
        c = points[2, :]

        B = b - a
        F = c - b
        A = F - B
        nF = np.linalg.norm(F)
        nA = np.linalg.norm(A)
        nB = np.linalg.norm(B)
        if nA > 1e-8:
            L = (nF * np.dot(A, F) - nB * np.dot(A, B)) / (nA ** 2) + (nA ** 2 * nB ** 2 - np.dot(A, B) ** 2) / \
                (nA ** 3) * (np.log(nA * nF + np.dot(A, F)) - np.log(nA * nB + np.dot(A, B)))
            return L
        else:
            return np.linalg.norm(a - c)

    def calc_len_with_quads(self):
        L = 0
        for k in range(self.path.get_num_curves()):
            points = self.path.get_nth_curve_points(k)
            quads = self.cubic_to_quads(points)
            L0 = self.calc_len_bezier_quad(quads[:3, :])
            L1 = self.calc_len_bezier_quad(quads[3:, :])
            L += L0 + L1
        return L

    def get_path_length(self):
        return self.pathdata_lengths[-1]

    def alpha_from_length(self, s):
        if hasattr(s, '__iter__'):
            return [np.interp(t, self.pathdata_lengths, self.pathdata_alpha) for t in s]
        else:
            return np.interp(s, self.pathdata_lengths, self.pathdata_alpha)

    def length_from_alpha(self, a):
        if hasattr(a, '__iter__'):
            return [np.interp(t, self.pathdata_alpha, self.pathdata_lengths) for t in a]
        else:
            return np.interp(a, self.pathdata_alpha, self.pathdata_lengths)

    def equalize_alpha(self, a):
        'used for inverting the alpha behavior'
        return self.alpha_from_length(a * self.get_path_length())

    def equalize_rate_func(self, rate_func):
        '''
        Specifically made to be used with Create() animation.
        :param rate_func: rate function to be equalized
        :return: callable new rate function
        Example:
        class test_path_mapper_anim(Scene):
            def construct(self):
                mob1 = round_corners(Triangle(fill_color=TEAL,fill_opacity=0).scale(3),0.5)
                PM = Path_mapper(mob1)
                mob2 = mob1.copy()
                mob1.shift(LEFT * 2.5)
                mob2.shift(RIGHT * 2.5)

                self.play(Create(mob1,rate_func=PM.equalize_rate_func(smooth)),Create(mob2),run_time=5)
                self.wait()
        '''

        def eq_func(t: float):
            return self.equalize_alpha(rate_func(t))

        return eq_func

    def point_from_proportion(self, alpha: float) -> np.ndarray:
        '''
         Override original implementation.
         Should be the same, except it uses pre calculated length table and should be faster a bit.
        '''
        if hasattr(alpha, '__iter__'):
            values = self.alpha_from_length(alpha * self.get_path_length())
            ret = np.empty((0, 3))
            for a in values:
                if a == 1:
                    index = self.path.get_num_curves() - 1
                    remainder = 1
                else:
                    index = int(a * self.path.get_num_curves() // 1)
                    remainder = (a * self.path.get_num_curves()) % 1
                p = self.path.get_nth_curve_function(index)(remainder)
                ret = np.concatenate([ret, np.reshape(p, (1, 3))], axis=0)
            return ret
        else:
            a = self.alpha_from_length(alpha * self.get_path_length())
            if a == 1:
                index = self.path.get_num_curves() - 1
                remainder = 1
            else:
                index = int(a * self.path.get_num_curves() // 1)
                remainder = (a * self.path.get_num_curves()) % 1
            return self.path.get_nth_curve_function(index)(remainder)

    def get_length_between_points(self, b, a):
        '''
        Signed arc length between to points.
        :param b: second point
        :param a: first point
        :return: length (b-a)
        '''
        return self.length_from_alpha(b) - self.length_from_alpha(a)

    def get_length_between_points_wrapped(self, b, a):
        ''' This function wraps around the length between two points similar to atan2 method.
        Useful for closed mobjects.
        Returns distance value between -L/2...L/2 '''
        AB = self.get_length_between_points(b, a)
        L = self.get_path_length()
        return (AB % L - L / 2) % L - L / 2

    def get_length_between_points_tuple(self, b, a):
        ''' Function to get the 2 absolute lengths between 2 parameters on closed mobjects.
        Useful for closed mobjects.
        :returns tuple (shorter, longer)'''

        AB = abs(self.get_length_between_points(b, a))
        L = self.get_path_length()
        if AB > L / 2:
            return (L - AB), AB
        else:
            return AB, (L - AB)

    def get_bezier_index_from_length(self, s):
        a = self.alpha_from_length(s)
        nc = self.path.get_num_curves()
        indx = int(a * nc // 1)
        bz_a = a * nc % 1
        if indx == nc:
            indx = nc - 1
            bz_a = 1
        return (indx, bz_a)

    def get_tangent_unit_vector(self, s):
        # diff_bez_points = 1/3*(self.path.points[1:,:]-self.path.points[:-1,:])
        indx, bz_a = self.get_bezier_index_from_length(s)
        points = self.path.get_nth_curve_points(indx)
        dpoints = (points[1:, :] - points[:-1, :]) / 3
        bzf = bezier(dpoints)
        point = bzf(bz_a)
        return normalize(point)

    def get_tangent_angle(self, s):
        tv = self.get_tangent_unit_vector(s)
        return angle_of_vector(tv)

    def get_normal_unit_vector(self, s):
        tv = self.get_tangent_unit_vector(s)
        return rotate_vector(tv, PI / 2)

    def get_curvature_vector(self, s):
        ind, bz_a = self.get_bezier_index_from_length(s)
        points = self.path.get_nth_curve_points(ind)
        dpoints = (points[1:, :] - points[:-1, :]) * 3
        ddpoints = (dpoints[1:, :] - dpoints[:-1, :]) * 2
        deriv = bezier(dpoints)(bz_a)
        dderiv = bezier(ddpoints)(bz_a)
        return np.cross(deriv, dderiv) / (np.linalg.norm(deriv) ** 3)

    def get_curvature(self, s):
        return np.linalg.norm(self.get_curvature_vector(s))


class DashedMObject(VDict):
    def __init__(self, target_mobject: VMobject,
                 num_dashes=15,
                 dashed_ratio=0.5,
                 dash_offset=0.0,
                 **kwargs):
        super().__init__(**kwargs)
        self.path = PathMapper(target_mobject, num_of_path_points=10 * target_mobject.get_num_curves())

        dashes = self.dash_objects(num_dashes, dash_ratio=dashed_ratio, offset=dash_offset)
        self.add({'dashes': dashes})
        self['dashes'].match_style(target_mobject)

    def dash_objects(self, num_dashes, dash_ratio=0.5, offset=0.0):
        full_len = self.path.get_path_length()  # 线段总长
        period = full_len / num_dashes  # 每段长度
        dash_len = period * dash_ratio  # 每段dash长度
        n = num_dashes + 3  # 冗余处理
        offset = offset - int(offset / period) * period

        dash_starts = [max(((i - 1) * period + offset), 0) for i in range(n)]
        dash_ends = [((i - 1) * period + dash_len + offset) for i in range(n)]

        ref_mob = self.path.path
        start_list = self.path.alpha_from_length(dash_starts)
        end_list = self.path.alpha_from_length(dash_ends)
        ret = []
        for i in range(len(dash_starts)):
            mob_copy = VMobject().match_points(ref_mob)
            ret.append(mob_copy.pointwise_become_partial(mob_copy,
                                                         float(start_list[i]),
                                                         float(end_list[i])
                                                         )
                       )
        return VGroup(*ret)


class WeightMatrix(DecimalMatrix):
    def __init__(self,
                 length: int = 7,
                 shape: Optional[Tuple[int, int]] = None,
                 value_range: tuple[float, float] = (-9.9, 9.9)):

        if shape is None:
            shape = (length, 1)
        self.shape = shape
        self.value_range = value_range
        values = np.random.uniform(*self.value_range, size=shape)
        # values = np.zeros(shape=shape)
        super().__init__(values)
        self.reset_entry_colors()

    def reset_entry_colors(self):
        for entry in self.get_entries():
            entry.set_color(
                color=value_to_color(entry.get_value(), min_value=0, max_value=max(self.value_range))
            )
        return self


class RandomizeMatrixEntries(Animation):
    def __init__(self, matrix, **kwargs):
        self.matrix = matrix
        self.entries = matrix.get_entries()
        self.start_values = [entry.get_value() for entry in self.entries]

        # todo: 不完美
        self.target_values = [np.random.uniform(0, matrix.value_range[1]) if x > 0
                              else np.random.uniform(matrix.value_range[0], 0) for x in self.start_values]
        # self.target_values = [1.0 for x in self.start_values]
        super().__init__(matrix, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        for index, entry in enumerate(self.entries):
            start = self.start_values[index]
            target = self.target_values[index]
            sub_alpha = self.get_sub_alpha(alpha, index, len(self.entries))
            entry.set_value(interpolate(start, target, sub_alpha))

        self.matrix.reset_entry_colors()


class ContextAnimation(LaggedStart):
    def __init__(self,
                 target,
                 sources,
                 direction=UP,
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
            arcs.add(Line(
                source.get_edge_center(direction),
                target.get_edge_center(direction),
                path_arc=sign * path_arc,
                stroke_color=random_bright_color(),
                stroke_width=interpolate(
                    min_stroke_width,
                    max_stroke_width,
                    strength,
                )
            ))
        if fix_in_frame:
            arcs.fix_in_frame()
        arcs.shuffle()
        lag_ratio = 0.5 / len(arcs) if lag_ratio is None else lag_ratio

        super().__init__(
            *(
                ShowPassingFlashWithThinningStrokeWidth(arc, time_width=time_width)
                for arc in arcs
            ),
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )


class Diffusion(ThreeDScene):
    def __init__(self):
        super().__init__()
        self.gear = SVGMobject("assets/wheel.svg")
        # models
        # -----------------------------
        self.gears_diffusion = VGroup(
            self.gear.copy().scale(0.5).shift(0.78 * UP).set_color(YELLOW_E),
            self.gear.copy().scale(0.5).shift(0.57 * LEFT).set_color(ORANGE),
            self.gear.copy().scale(0.5).shift(0.57 * RIGHT).set_color(BLUE_D)
        )
        text_diffusion = Text(
            "Diffusion Model", font="Menlo", font_size=20, color=GREY
        ).next_to(self.gears_diffusion, DOWN, SMALL_BUFF)
        self.model_diffusion = VGroup(
            self.gears_diffusion, text_diffusion,
            SurroundingRectangle(
                VGroup(self.gears_diffusion, text_diffusion),
                buff=0.2, color=GREY, corner_radius=0.3, stroke_width=2.0
            )
        )
        # -----------------------------
        self.gears_clip = VGroup(
            self.gear.copy().scale(0.5).shift(0.8 * UP).rotate(10 * DEGREES).set_color(BLUE_C),
            self.gear.copy().scale(0.5).shift(0.55 * RIGHT).rotate(-8 * DEGREES).set_color(BLUE_E)
        )
        text_clip = Text(
            "CLIP Model", font="Menlo", font_size=20, color=GREY
        ).next_to(self.gears_clip, DOWN, SMALL_BUFF)
        self.model_clip = VGroup(
            self.gears_clip, text_clip,
            SurroundingRectangle(
                VGroup(self.gears_clip, text_clip),
                buff=0.2, color=GREY, corner_radius=0.3, stroke_width=2.0
            )
        )
        # -----------------------------
        self.gears_text_encoder = VGroup(self.gear.copy().scale(0.4).set_color(BLUE_C))
        text_text_encoder = Text(
            "Text Encoder", font="Menlo", font_size=14, color=GREY
        ).next_to(self.gears_text_encoder, DOWN, SMALL_BUFF)
        self.model_text_encoder = VGroup(
            self.gears_text_encoder, text_text_encoder,
            SurroundingRectangle(
                VGroup(self.gears_text_encoder, text_text_encoder),
                buff=0.1, color=GREY, corner_radius=0.15, stroke_width=2.0
            )
        )

        self.gears_image_encoder = VGroup(self.gear.copy().scale(0.4).set_color(BLUE_E))
        text_image_encoder = Text(
            "Image Encoder", font="Menlo", font_size=14, color=GREY
        ).next_to(self.gears_image_encoder, DOWN, SMALL_BUFF)
        self.model_image_encoder = VGroup(
            self.gears_image_encoder, text_image_encoder,
            SurroundingRectangle(
                VGroup(self.gears_image_encoder, text_image_encoder),
                buff=0.1, color=GREY, corner_radius=0.15, stroke_width=2.0
            )
        )

        # -----------------------------
        trapezoid_right = Polygon(
            (0.04, 0.4, 0), (1.0, 0.9, 0), (1.0, -0.9, 0), (0.04, -0.4, 0),
            stroke_color=GREY, stroke_width=2.0
        )
        trapezoid_left = Polygon(
            (-0.04, 0.4, 0), (-1.0, 0.9, 0), (-1.0, -0.9, 0), (-0.04, -0.4, 0),
            stroke_color=GREY, stroke_width=2.0
        )
        self.gears_vqvae = VGroup(
            self.gear.copy().scale(0.4).shift(0.52 * LEFT).set_color(GOLD_C),
            self.gear.copy().scale(0.4).shift(0.52 * RIGHT).set_color(GREEN_C)
        )
        text_vqvae = Text(
            "VQVAE", font="Menlo", font_size=20, color=GREY
        ).shift(0.8 * DOWN)
        self.model_vqvae = VGroup(
            self.gears_vqvae, trapezoid_right, trapezoid_left, text_vqvae,
            SurroundingRectangle(
                VGroup(trapezoid_right, trapezoid_left, text_vqvae),
                buff=0.15, color=GREY, corner_radius=0.3, stroke_width=2.0
            )
        )

        self.gears_vae_encoder = VGroup(
            self.gear.copy().scale(0.4).set_color(GOLD_C)
        )
        text_vae_encoder = Text(
            "VQVAE \nEncoder", font="Menlo", color=GREY
        ).scale(0.3).next_to(self.gears_vae_encoder, DOWN, SMALL_BUFF)
        self.model_vae_encoder = VGroup(
            self.gears_vae_encoder, text_vae_encoder,
            SurroundingRectangle(
                VGroup(self.gears_vae_encoder, text_vae_encoder),
                buff=0.1, color=GREY, corner_radius=0.15, stroke_width=2.0
            )
        )

        self.gears_vae_decoder = VGroup(
            self.gear.copy().scale(0.4).set_color(GREEN_C)
        )
        text_vae_decoder = Text(
            "VQVAE \nDecoder", font="Menlo", color=GREY
        ).scale(0.3).next_to(self.gears_vae_decoder, DOWN, SMALL_BUFF)
        self.model_vae_decoder = VGroup(
            self.gears_vae_decoder, text_vae_decoder,
            SurroundingRectangle(
                VGroup(self.gears_vae_decoder, text_vae_decoder),
                buff=0.1, color=GREY, corner_radius=0.15, stroke_width=2.0
            )
        )

        # ==============================================================
        # title
        self.title = Text("How does diffusion model work")
        self.logo = MathTex(
            r"\mathbb{JAYANDJEAN}", fill_color="#ece6e2"
        ).next_to(self.title, DOWN, buff=0.5).scale(1.2)
        self.title_clip = Text("CLIP", font="Menlo").to_edge(UL, buff=0.5).scale(0.7)
        self.title_ddpm = Text("DDPM", font="Menlo").to_edge(UL, buff=0.5).scale(0.7)
        self.title_latent = Text("Latent", font="Menlo").to_edge(UL, buff=0.5).scale(0.7)

        text_prompt = Paragraph("a cyberpunk with ",
                                "natural greys and ",
                                "whites and browns.",
                                line_spacing=1.0, font="Menlo").scale(0.4)
        surrounding_prompt = SurroundingRectangle(
            text_prompt, buff=0.2, color=WHITE, corner_radius=0.3, stroke_width=0.5)
        self.prompt = VGroup(surrounding_prompt, text_prompt)

        # ==============================================================

        prism1 = Group(*[SVGMobject("assets/prism1.svg").scale(2.0) for i in range(3)])
        prism1.arrange(RIGHT, buff=-0.6).move_to(5.5 * LEFT)
        prism2 = Group(*[SVGMobject("assets/prism2.svg").scale(1.2) for i in range(2)])
        prism2.arrange(RIGHT, buff=-0.3).next_to(prism1, RIGHT, buff=-0.6).align_to(prism1, DOWN)
        prism3 = Group(*[SVGMobject("assets/prism3.svg").scale(0.7) for i in range(2)])
        prism3.arrange(RIGHT, buff=-0.1).next_to(prism2, RIGHT, buff=-0.3).align_to(prism1, DOWN)
        prism4 = Group(*[SVGMobject("assets/prism4.svg").scale(0.3) for i in range(4)])
        prism4[2].set_color(GOLD_A)
        prism4.arrange(RIGHT, buff=-0.01).next_to(prism3, RIGHT, buff=-0.1).align_to(prism1, DOWN)
        prism5 = Group(*[SVGMobject("assets/prism3.svg").scale(0.7) for i in range(2)])
        prism5.arrange(RIGHT, buff=-0.1).next_to(prism4, RIGHT, buff=0.0).align_to(prism1, DOWN)
        prism6 = Group(*[SVGMobject("assets/prism2.svg").scale(1.2) for i in range(2)])
        prism6.arrange(RIGHT, buff=-0.3).next_to(prism5, RIGHT, buff=-0.1).align_to(prism1, DOWN)
        prism7 = Group(*[SVGMobject("assets/prism1.svg").scale(2.0) for i in range(4)])
        prism7.arrange(RIGHT, buff=-0.6).next_to(prism6, RIGHT, buff=-0.3).align_to(prism1, DOWN)

        delta_x = 0.3
        delta_y = 0.5
        lines_concat = VGroup()
        for rate, p1, p2 in [(0.75, prism1, prism7), (0.5, prism2, prism6), (0.3, prism3, prism5)]:
            p10_start = (p1[-1].get_right() - p1[-1].get_center()) * rate + p1[-1].get_top()
            p10_end = p10_start + delta_x * RIGHT + delta_y * UP
            p11_start = (p2[0].get_right() - p2[0].get_center()) * rate + p2[0].get_top()
            p11_end = p11_start + delta_x * RIGHT + delta_y * UP
            lines_concat.add(Line(p10_start, p10_end, color=GREY, stroke_width=2.0))
            lines_concat.add(Line(p10_end, p11_end, color=GREY, stroke_width=2.0))
            lines_concat.add(Line(p11_start, p11_end, color=GREY, stroke_width=2.0))
        text_concat1 = Text("Concatenate", font="Menlo", color=GREY).scale(0.3).next_to(lines_concat[1], DOWN)
        text_concat2 = Text("···", font="Menlo", color=GREY).scale(0.3).next_to(lines_concat[4], UP)
        text_unet = Text("UNet", font="Menlo", color=GREY).scale(0.6).next_to(prism4, UP)

        self.unet = Group(
            Group(prism1, prism2, prism3, prism4, prism5, prism6, prism7),
            lines_concat,
            text_concat1, text_concat2,
            # text_unet
        ).scale(0.5)
