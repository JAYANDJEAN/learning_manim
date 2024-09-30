from PIL import Image

from utils import *


class Models(Diffusion):
    def __init__(self):
        super().__init__()

    def ddpm1(self):
        # show demo
        image_text_pair1 = Group(
            ImageMobject(f"shows/show_001.jpg").set(height=4),
            ImageMobject(f"shows/show_002.jpg").set(height=4)
        ).arrange(RIGHT, buff=0.01)
        image_text_pair2 = Group(
            ImageMobject(f"shows/show_003.jpg").set(height=4),
            ImageMobject(f"shows/show_004.jpg").set(height=4)
        ).arrange(RIGHT, buff=0.01)
        image_text_pair = Group(image_text_pair1, image_text_pair2).arrange(DOWN, buff=0.03)
        products = Group(
            ImageMobject(f"assets/product_mid.jpg").set(height=2.2),
            ImageMobject(f"assets/product_sd3.png").set(height=2.2),
            ImageMobject(f"assets/product_flux.png").set(height=2.2)
        ).arrange(RIGHT, buff=0.3)
        self.play(
            FadeIn(image_text_pair1[0], shift=RIGHT),
            FadeIn(image_text_pair1[1], shift=DOWN),
            FadeIn(image_text_pair2[1], shift=LEFT),
            FadeIn(image_text_pair2[0], shift=UP),
            run_time=2
        )
        self.play(FadeOut(image_text_pair, shift=LEFT))
        self.play(LaggedStartMap(SpinInFromNothing, products, lag_ratio=0.5))
        self.play(FadeOut(products, shift=LEFT))

        # 3. show generating shows
        image_prompt = ImageMobject("assets/prompt.png").set(width=4.2)

        embedding_prompt = WeightMatrix(length=15).set(width=0.5)
        matrix_image = VGroup(
            WeightMatrix(shape=(14, 8)).set(width=4).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP),
            WeightMatrix(shape=(14, 8)).set(width=4).set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP),
            WeightMatrix(shape=(14, 8)).set(width=4),
        )

        Group(self.prompt, embedding_prompt, self.model_diffusion, matrix_image).arrange(RIGHT, buff=1.0)
        arrow_prompt_embedding = Arrow(self.prompt.get_right(), embedding_prompt.get_left())
        arrow_embedding_model = Arrow(embedding_prompt.get_right(), self.model_diffusion.get_left())
        arrow_model_matrix = Arrow(self.model_diffusion.get_right(), matrix_image.get_left())
        image_prompt.move_to(matrix_image.get_center())

        self.play(GrowFromCenter(self.model_diffusion))
        self.play(Create(self.prompt))
        self.play(
            GrowArrow(arrow_prompt_embedding),
            Indicate(embedding_prompt)
        )
        self.play(
            GrowArrow(arrow_embedding_model),
            AnimationGroup(
                Rotate(self.gears_diffusion[i], axis=IN if i == 0 else OUT,
                       about_point=self.gears_diffusion[i].get_center())
                for i in range(3)
            ), run_time=3
        )
        self.play(GrowArrow(arrow_model_matrix), Create(matrix_image))
        self.play(FadeIn(image_prompt, shift=DOWN), FadeOut(matrix_image))
        self.play(FadeOut(image_prompt, arrow_prompt_embedding, arrow_embedding_model, arrow_model_matrix, self.prompt))
        self.wait()

        # 3.1. why we need embedding
        self.model_diffusion.generate_target()
        box = Rectangle(width=9.5, height=4.5).set_fill(GREY_E, 1).set_stroke(WHITE, 1)
        VGroup(self.model_diffusion.target, box).arrange(RIGHT, buff=1)
        line1 = Line(start=self.model_diffusion.target.get_corner(direction=UR),
                     end=box.get_corner(direction=UL)).set_stroke(WHITE, 1)
        line2 = Line(start=self.model_diffusion.target.get_corner(direction=DR),
                     end=box.get_corner(direction=DL)).set_stroke(WHITE, 1)

        self.play(Wiggle(embedding_prompt))
        self.play(FadeOut(embedding_prompt), MoveToTarget(self.model_diffusion))
        self.play(LaggedStartMap(Create, VGroup(box, line1, line2)))

        matrix1, matrix2, matrix3 = [
            VGroup(WeightMatrix(shape=shape).set(width=0.4 * shape[1]),
                   WeightMatrix(shape=shape).set(width=0.4 * shape[1])
                   .set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP),
                   WeightMatrix(shape=shape).set(width=0.4 * shape[1])
                   .set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP)
                   ) for shape in [(8, 6), (6, 6), (8, 6)]]
        eq = Tex('=')
        mul = Tex('*')
        all_matrix = VGroup(matrix1, mul, matrix2, eq, matrix3).arrange(RIGHT, buff=0.1).move_to(box.get_center())
        self.play(LaggedStartMap(FadeIn, VGroup(matrix1, mul, matrix2, eq, matrix3), lag_ratio=0.01, run_time=0.5))
        for i in range(3):
            self.play(
                LaggedStartMap(RandomizeMatrixEntries, VGroup(matrix1[0], matrix2[0], matrix3[0]), lag_ratio=0.1),
                AnimationGroup(
                    Rotate(self.gears_diffusion[i],
                           axis=IN if i == 0 else OUT,
                           about_point=self.gears_diffusion[i].get_center())
                    for i in range(3)
                ), run_time=2,
            )
        self.play(FadeOut(all_matrix))
        self.play(FadeOut(box, line1, line2, self.model_diffusion))
        self.wait()

        # 3.2. what is the image
        image_prompt.move_to(4 * LEFT)
        image_rgb = Group(
            ImageMobject("assets/prompt_r.png").set(width=4.0).set_opacity(0.8),
            ImageMobject("assets/prompt_g.png").set(width=4.0).set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP),
            ImageMobject("assets/prompt_b.png").set(width=4.0).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP)
        ).move_to(2 * RIGHT)
        arrow_images = Arrow(image_prompt.get_right(), image_rgb.get_left())
        self.play(FadeIn(image_prompt, shift=RIGHT), GrowArrow(arrow_images))
        self.play(LaggedStartMap(FadeIn, image_rgb, shift=DOWN, lag_ratio=1.0))
        self.play(FadeOut(image_prompt, arrow_images))

        image_rgb.generate_target()
        image_rgb.target.arrange(RIGHT, buff=0.4).set(opacity=1.0)
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
        )
        lattice.set(width=4.0)
        lattices = VGroup(lattice.copy(), lattice.copy(), lattice.copy()).arrange(RIGHT, buff=0.4)
        eq = Text("=").scale(3)
        image_eq = Group(matrix_image, eq, image_prompt).arrange(RIGHT, buff=0.5)
        matrix_image_show = VGroup(
            WeightMatrix(shape=(14, 8)).set(width=4),
            WeightMatrix(shape=(14, 8)).set(width=4),
            WeightMatrix(shape=(14, 8)).set(width=4)
        ).arrange(RIGHT, buff=0.4)
        matrix_image_show.generate_target()
        matrix_image_show.target = matrix_image

        self.play(MoveToTarget(image_rgb))
        self.play(FadeIn(lattices))
        self.play(
            FadeTransform(lattices, matrix_image_show),
            FadeOut(image_rgb)
        )
        self.play(
            MoveToTarget(matrix_image_show),
            Create(eq),
            FadeIn(image_prompt, shift=LEFT)
        )
        self.play(FadeOut(image_eq, matrix_image_show))
        self.wait()

    def ddpm2(self):
        # 4. 目录
        # 清理干净
        title_papers = VGroup(
            Text("2020.06 \nDenoising Diffusion Probabilistic Models",
                 font="Menlo", t2c={'D': YELLOW_E, 'P': YELLOW_E, 'M': YELLOW_E}),
            Text("2021.03 \nContrastive Language-Image Pre-Training",
                 font="Menlo", t2c={'C': YELLOW_E, 'L': YELLOW_E, 'I': YELLOW_E, 'P': YELLOW_E}),
            Text("2021.12 \nLatent Diffusion Models", font="Menlo"),
            Text("2024.03 \nStable Diffusion 3", font="Menlo"),
        )
        image_papers = Group(
            ImageMobject("assets/paper_ddpm.png").set(height=1),
            ImageMobject("assets/paper_clip.png").set(height=0.9),
            ImageMobject("assets/paper_ldm.png").set(height=0.9),
            ImageMobject("assets/paper_sd3.png").set(height=1)
        )
        arrow_history = Arrow(4 * UP, 4 * DOWN).move_to(4 * LEFT)
        dot_papers = VGroup(*[Dot(radius=0.1) for _ in range(4)]).arrange(DOWN, buff=1.5).move_to(4 * LEFT + 0.5 * UP)
        for dot, title, im in zip(dot_papers, title_papers, image_papers):
            title.scale(0.35).next_to(dot, direction=RIGHT, buff=0.1)
            im.scale(0.8).next_to(title, direction=DOWN, buff=0.1, aligned_edge=LEFT)

        self.play(GrowArrow(arrow_history))
        self.play(Succession(*[FadeIn(Group(dot_papers[i], title_papers[i], image_papers[i])) for i in range(4)]))
        self.wait()

        # 5. DDPM
        self.model_diffusion.move_to(ORIGIN)

        text_prompt_cat = Text("a photo of a cat", font="Menlo").scale(0.4)
        surrounding_prompt_cat = SurroundingRectangle(text_prompt_cat,
                                                      buff=0.1, color=WHITE, corner_radius=0.1).set_stroke(width=0.5)
        prompt_cat = VGroup(text_prompt_cat, surrounding_prompt_cat).move_to(3 * UP)
        arrow_prompt_model = Arrow(prompt_cat.get_bottom(), self.model_diffusion.get_top())
        image_noise = ImageMobject("cat_with_noise/cat_140.jpg").set(width=4).move_to(4.5 * LEFT)
        image_cat_35 = ImageMobject("cat_with_noise/cat_020.jpg").set(width=4).move_to(4.5 * LEFT)
        image_cat = ImageMobject("cat_with_noise/cat_000.jpg").set(width=4).move_to(4.5 * RIGHT)
        arrow_noise_model = Arrow(image_noise.get_right(), self.model_diffusion.get_left())
        arrow_model_cat = Arrow(self.model_diffusion.get_right(), image_cat.get_left())
        hard = Text("Hard!").scale(0.9).move_to(3 * RIGHT + 2.5 * UP)
        easy = Text("Easy!").scale(0.9).move_to(3 * RIGHT + 2.5 * UP)
        self.play(
            FadeOut(image_papers),
            FadeTransform(VGroup(title_papers, arrow_history, dot_papers), self.title_ddpm)
        )
        self.play(GrowFromCenter(self.model_diffusion))
        self.play(FadeIn(image_noise, shift=DOWN), Write(prompt_cat))
        self.play(
            GrowArrow(arrow_noise_model),
            GrowArrow(arrow_prompt_model),
            AnimationGroup(
                Rotate(self.gears_diffusion[i], axis=IN if i == 0 else OUT,
                       about_point=self.gears_diffusion[i].get_center())
                for i in range(3)
            ), run_time=2
        )
        self.play(GrowArrow(arrow_model_cat), FadeIn(image_cat, shift=DOWN))
        self.play(Indicate(hard))
        self.play(FadeOut(image_noise, shift=DOWN))
        self.play(FadeIn(image_cat_35, shift=DOWN), FadeOut(hard))
        self.play(Indicate(easy))
        self.play(FadeOut(easy, arrow_model_cat, self.model_diffusion, arrow_noise_model,
                          arrow_prompt_model, prompt_cat))
        self.wait()

        # 5.1 Decode
        path_cats = ([f"cat_with_noise/cat_{i:03}.jpg" for i in range(0, 150, 10)])
        image_cats_decode_15 = Group(
            *[Group(
                *[ImageMobject(path_cats[j]) for j in range(i * 5, (i + 1) * 5)]
            ).set(height=1.8).arrange(LEFT if i != 1 else RIGHT, buff=0.4) for i in range(3)]
        ).arrange(DOWN, buff=0.4).shift(0.5 * DOWN)

        image_cats_decode_5 = Group(
            *([ele for i in [f"cat_with_noise/{f}" for f in ['cat_140.jpg', 'cat_100.jpg',
                                                             'cat_060.jpg', 'cat_020.jpg']]
               for ele in [ImageMobject(i).set(height=1.9), Text("···").scale(0.7)]] +
              [ImageMobject("cat_with_noise/cat_000.jpg").set(height=1.9)]
              )
        ).arrange(RIGHT, buff=0.35)

        self.play(
            FadeTransform(image_cat_35, image_cats_decode_15[0][1]),
            FadeTransform(image_cat, image_cats_decode_15[0][0])
        )
        arrow_between_images = []
        for i, image_group in enumerate(image_cats_decode_15):
            j = 0
            time1 = 0.7
            time2 = 0.3
            line_width = 2.5
            tip_length = 0.15
            for j in range(len(image_group) - 1):
                arr = Arrow(image_group[j + 1].get_right(), image_group[j].get_left(),
                            stroke_width=line_width, tip_length=tip_length,
                            max_tip_length_to_length_ratio=1.0,
                            max_stroke_width_to_length_ratio=20
                            ) \
                    if i != 1 else Arrow(image_group[j + 1].get_left(), image_group[j].get_right(),
                                         stroke_width=line_width, tip_length=tip_length,
                                         max_tip_length_to_length_ratio=1.0,
                                         max_stroke_width_to_length_ratio=20)
                arrow_between_images.append(arr)
                if i == 0 and j <= 1:
                    self.play(GrowArrow(arr, run_time=time1))
                else:
                    self.play(FadeIn(image_group[j], run_time=time1 if i == 0 else time2),
                              GrowArrow(arr, run_time=time1 if i == 0 else time2))

            self.play(FadeIn(image_group[j + 1], run_time=time1 if i == 0 else time2))
            if i == 0:
                arr = CubicBezier(image_cats_decode_15[i + 1][0].get_left(),
                                  image_cats_decode_15[i + 1][0].get_left() + 0.3 * LEFT,
                                  image_group[j + 1].get_left() + 0.3 * LEFT,
                                  image_group[j + 1].get_left(), stroke_width=line_width)
                arrow_between_images.append(arr)
                self.play(Create(arr, run_time=time1))
            elif i == 1:
                arr = CubicBezier(image_cats_decode_15[i + 1][0].get_right(),
                                  image_cats_decode_15[i + 1][0].get_right() + 0.3 * RIGHT,
                                  image_group[j + 1].get_right() + 0.3 * RIGHT,
                                  image_group[j + 1].get_right(), stroke_width=line_width)
                arrow_between_images.append(arr)
                self.play(Create(arr, run_time=time2))

        images_and_lines = Group(image_cats_decode_15, Group(*arrow_between_images))
        images_and_lines.generate_target()
        images_and_lines.target.scale(0.8).to_edge(RIGHT)
        brace_images_and_lines = Brace(images_and_lines.target, direction=LEFT, buff=0.1)
        brace_images_and_lines.generate_target()
        brace_images_and_lines.target = Brace(image_cats_decode_5, direction=UP, buff=0.1)
        text_images_and_lines = Text("Decode").next_to(brace_images_and_lines, LEFT)

        self.play(MoveToTarget(images_and_lines))
        self.play(GrowFromCenter(brace_images_and_lines), Write(text_images_and_lines))
        # 特殊处理，方便做transform
        image_cats_decode_15 = Group(*[i for group in image_cats_decode_15 for i in group])
        image_cats_decode_5_image = Group(*[i for i in image_cats_decode_5 if isinstance(i, ImageMobject)])
        image_cats_decode_5_text = Group(*[i for i in image_cats_decode_5 if isinstance(i, Text)])
        brace_images_and_lines.generate_target()
        brace_images_and_lines.target = Brace(image_cats_decode_5, direction=UP, buff=0.1)
        self.play(
            FadeOut(VGroup(*arrow_between_images)),
            Transform(image_cats_decode_15, image_cats_decode_5_image, replace_mobject_with_target_in_scene=True),
            FadeIn(image_cats_decode_5_text),
            MoveToTarget(brace_images_and_lines),
            text_images_and_lines.animate.next_to(brace_images_and_lines.target, UP)
        )
        self.wait()

        # 5.2 Encode
        image_cats_encode_decode_5 = Group(
            *([ele for i in [f"cat_with_noise/{f}" for f in
                             ['cat_000.jpg', 'cat_040.jpg', 'cat_150.jpg', 'cat_040.jpg']]
               for ele in [ImageMobject(i).set(height=1.9), Text("···").scale(0.7)]] +
              [ImageMobject("cat_with_noise/cat_000.jpg").set(height=1.9)]
              )
        ).arrange(RIGHT, buff=0.35)

        image_cats_encode_5 = Group(
            *([ele for i in [f"cat_with_noise/{f}" for f in
                             ['cat_000.jpg', 'cat_030.jpg', 'cat_060.jpg', 'cat_090.jpg']]
               for ele in (ImageMobject(i).set(height=1.9), Text("···").scale(0.7))] +
              [ImageMobject("cat_with_noise/cat_150.jpg").set(height=1.9)]
              )
        ).arrange(RIGHT, buff=0.35)

        formula_xt = MathTex(r"\mathbf{x}_t=\sqrt{\bar{\alpha}_t} ",
                             r"\mathbf{x}_0",
                             r"+\sqrt{1-\bar{\alpha}_t} ",
                             r"\boldsymbol{\epsilon}")
        brace_decode = Brace(image_cats_encode_decode_5[4:], direction=UP, buff=0.1)
        brace_encode = Brace(image_cats_encode_decode_5[:5], direction=DOWN, buff=0.1)
        text_encode = Text("Encode").next_to(brace_encode, DOWN)
        brace_encode_only = Brace(image_cats_encode_5, direction=DOWN, buff=0.1)
        text_encode_steps = Text("1000 Steps").next_to(brace_encode_only, DOWN)
        formula_xt.next_to(text_encode_steps, DOWN)
        frame_box_xt = SurroundingRectangle(formula_xt[1], corner_radius=0.01).set_stroke(width=2.0)
        frame_box_noise = SurroundingRectangle(formula_xt[3], corner_radius=0.01).set_stroke(width=2.0)
        arrow_xt_image = Arrow(frame_box_xt.get_bottom(), image_cats_encode_5[0].get_bottom(),
                               path_arc=-90 * DEGREES, stroke_width=2.0, tip_length=0.2, buff=0.0)

        self.play(
            FadeTransform(brace_images_and_lines, brace_decode),
            text_images_and_lines.animate.next_to(brace_decode, UP),
            FadeOut(image_cats_decode_5_image, image_cats_decode_5_text),
            FadeIn(image_cats_encode_decode_5, shift=DOWN)
        )
        self.play(GrowFromCenter(brace_encode), Write(text_encode))

        self.play(FadeOut(brace_decode, text_images_and_lines))
        self.play(
            FadeOut(image_cats_encode_decode_5),
            FadeIn(image_cats_encode_5, shift=DOWN),
            FadeTransform(brace_encode, brace_encode_only)
        )

        self.play(FadeTransform(text_encode, text_encode_steps))
        self.play(Write(formula_xt))
        self.play(Create(frame_box_xt), GrowArrow(arrow_xt_image))
        self.play(Create(frame_box_noise))
        self.play(FadeOut(frame_box_xt, frame_box_noise, arrow_xt_image,
                          text_encode_steps, brace_encode_only, image_cats_encode_5))
        self.wait()

        # 5.3 encode x_t
        T = 1000
        betas = np.linspace(0.0001, 0.02, T)
        alphas = 1 - betas
        alphas_bar = np.cumprod(alphas)
        sqrt_alpha_bar = np.sqrt(alphas_bar)
        sqrt_one_minus_alpha_bar = np.sqrt(1 - alphas_bar)
        axes = Axes(
            x_range=[0, T, 100],
            y_range=[0, 1, 0.1],
            axis_config={"color": WHITE},
        ).add_coordinates().scale(0.9)

        alpha_curve = axes.plot_line_graph(
            x_values=np.arange(T),
            y_values=sqrt_alpha_bar,
            line_color=BLUE,
            stroke_width=4,
            add_vertex_dots=False
        )

        one_minus_alpha_curve = axes.plot_line_graph(
            x_values=np.arange(T),
            y_values=sqrt_one_minus_alpha_bar,
            line_color=RED,
            stroke_width=4,
            add_vertex_dots=False
        )
        line_50 = axes.get_vertical_line(axes.c2p(50, 1),
                                         line_config={"color": YELLOW_E, "dashed_ratio": 0.85})
        line_800 = axes.get_vertical_line(axes.c2p(800, 1),
                                          line_config={"color": YELLOW_E, "dashed_ratio": 0.85})

        alpha_50 = sqrt_alpha_bar[50]
        alpha_800 = sqrt_alpha_bar[800]
        one_minus_alpha_50 = sqrt_one_minus_alpha_bar[50]
        one_minus_alpha_800 = sqrt_one_minus_alpha_bar[800]
        dot_alpha_50 = Dot(axes.c2p(50, alpha_50), color=BLUE)
        dot_alpha_800 = Dot(axes.c2p(800, alpha_800), color=BLUE)
        dot_one_minus_alpha_50 = Dot(axes.c2p(50, one_minus_alpha_50), color=RED)
        dot_one_minus_alpha_800 = Dot(axes.c2p(800, one_minus_alpha_800), color=RED)

        alpha_label = MathTex(r"\sqrt{\bar{\alpha}_t}", color=BLUE).move_to(4.5 * RIGHT + 2 * DOWN)
        one_minus_alpha_label = MathTex(r"\sqrt{1 - \bar{\alpha}_t}", color=RED).move_to(4.5 * RIGHT + 2 * UP)
        image_cat_50 = ImageMobject("cat_with_noise/cat_040.jpg").set(height=2).next_to(line_50, RIGHT)
        image_cat_800 = ImageMobject("cat_with_noise/cat_200.jpg").set(height=2).next_to(line_800, LEFT)

        self.play(formula_xt.animate.to_edge(UP).scale(0.8))

        self.play(Create(axes))
        self.play(Create(alpha_curve), Write(alpha_label))
        self.play(Create(one_minus_alpha_curve), Write(one_minus_alpha_label))
        self.play(Create(line_50), Create(dot_alpha_50), Create(dot_one_minus_alpha_50))
        self.play(Create(line_800), Create(dot_alpha_800), Create(dot_one_minus_alpha_800))
        self.play(FadeIn(image_cat_50), FadeIn(image_cat_800))
        self.play(FadeOut(image_cat_50, image_cat_800))
        self.play(FadeOut(line_800, dot_alpha_800, dot_one_minus_alpha_800,
                          line_50, dot_alpha_50, dot_one_minus_alpha_50,
                          one_minus_alpha_curve, one_minus_alpha_label,
                          alpha_curve, alpha_label, axes, formula_xt))
        self.wait()

    def ddpm3(self):
        # 5.4 train model
        # 清理干净
        image_height = 1.8
        image_encode_set = Group(
            *[
                Group(
                    ImageMobject(f'cats/cat_{i}_000.jpg').set(height=image_height),
                    Text("···").scale(0.6),
                    ImageMobject(f'cats/cat_{i}_030.jpg').set(height=image_height),
                    Text("···").scale(0.6),
                    ImageMobject(f'cats/cat_{i}_060.jpg').set(height=image_height),
                    Text("···").scale(0.6),
                    ImageMobject(f'cats/cat_{i}_090.jpg').set(height=image_height),
                    Text("···").scale(0.6),
                    ImageMobject(f'cats/cat_{i}_150.jpg').set(height=image_height),
                ).arrange(RIGHT, buff=0.2)
                for i in range(2, 5)
            ]
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)

        image_encode_set.generate_target()
        image_encode_set.target.scale(0.5).to_edge(UP, buff=0.7)
        brace_image_set = Brace(image_encode_set.target, direction=DOWN)
        formula_encode = MathTex(
            r"\operatorname{loss}=|\boldsymbol{\epsilon}-",
            r"\boldsymbol{\epsilon}_\theta",
            r"(\mathbf{x}_t, t)\|^2"
        ).scale(0.7).next_to(brace_image_set, DOWN, buff=0.2)
        box_encode = SurroundingRectangle(
            formula_encode[1], corner_radius=0.01
        ).set_stroke(YELLOW_E, 2.0)
        self.unet.next_to(formula_encode, DOWN, buff=0.5)
        self.unet.generate_target()
        self.unet.target.move_to(ORIGIN)

        formula_decode = MathTex(
            r"\mathbf{x}_{t-1}",
            r"=",
            r"\frac{1}{\sqrt{\alpha_t}}\left(",
            r"\mathbf{x}_t-",
            r"\frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} ",
            r"\boldsymbol{\epsilon}_\theta",
            r"\left(\mathbf{x}_t, t\right)\right)+\sigma_t \mathbf{z}"
        ).scale(0.6).next_to(self.unet.target, DOWN, buff=0.5)
        box_decode = SurroundingRectangle(
            formula_decode[5], corner_radius=0.01
        ).set_stroke(YELLOW_E, 2.0)
        no_prompt = Text("No Prompt!").scale(0.5).next_to(formula_decode, DOWN)

        image_path_list = ([ImageMobject(f"cat_with_noise/cat_{i:03}.jpg").set(width=2)
                            for i in range(0, 255, 5)])
        image_output_cats = Group(*image_path_list[::-1])
        image_input_noise = (ImageMobject("cat_with_noise/cat_250.jpg").set(width=2)
                             .next_to(self.unet.target, LEFT, buff=1.0))
        image_output_dog = (ImageMobject("assets/dog.jpg").set(width=2)
                            .next_to(self.unet.target, RIGHT, buff=1.0))

        arrow_input_model = Arrow(image_input_noise.get_right(), self.unet.target.get_left())
        arrow_model_output = Arrow(self.unet.target.get_right(), image_output_dog.get_left())
        text_steps = VGroup(
            *[Text(f"Step {i + 1}", color=GREY).scale(0.6).next_to(self.unet.target, UP)
              for i in range(len(image_output_cats))
              ]
        )
        line_circle = CubicBezier(
            image_output_dog.get_center(),
            image_output_dog.get_center() + 4 * UP,
            image_input_noise.get_center() + 4 * UP,
            image_input_noise.get_center()
        ).set_stroke(GREY, 2.0)
        line_circle.z_index = -1

        # self.add(self.title_ddpm, image_encode_set.target,
        #          brace_image_set, formula_encode, box_encode, self.unet)
        # self.add(self.title_ddpm, self.unet.target, formula_decode, box_decode_model,
        #          image_input_noise, image_output_dog, arrow_input_model, arrow_model_output,
        #          text_steps[0], line_circle)

        self.play(LaggedStartMap(FadeIn, Group(*[i[0] for i in image_encode_set]), lag_ratio=0.5, shift=RIGHT))
        self.play(
            LaggedStart(
                *[
                    LaggedStartMap(FadeIn, Group(*[i for i in sub_set[1:]]), lag_ratio=0.1, shift=DOWN)
                    for sub_set in image_encode_set
                ]
            ),
            lag_ratio=0.5
        )
        self.play(MoveToTarget(image_encode_set), GrowFromCenter(brace_image_set))
        self.play(Write(formula_encode), Create(box_encode))
        self.play(FadeIn(self.unet))
        self.play(
            FadeOut(image_encode_set, box_encode, formula_encode, brace_image_set),
            MoveToTarget(self.unet)
        )
        self.play(Write(formula_decode), Create(box_decode))
        self.play(Write(no_prompt))
        self.wait()

        for i in range(len(image_output_cats) - 1):
            image_output_cats[i + 1].next_to(self.unet, RIGHT, buff=1.0)
            if i == 0:
                image_output_cats[i].next_to(self.unet, LEFT, buff=1.0)
                self.play(FadeIn(image_output_cats[i], shift=DOWN), GrowArrow(arrow_input_model))
                self.play(
                    FadeOut(image_output_cats[i], scale=0.1, target_position=self.unet.get_left()),
                    LaggedStart(
                        *[p.animate(rate_func=there_and_back).set_color(TEAL)
                          for prism in self.unet[0] for p in prism],
                        lag_ratio=0.1, run_time=1.5
                    )
                )
                self.play(
                    GrowArrow(arrow_model_output),
                    FadeIn(image_output_cats[i + 1], scale=0.1, target_position=self.unet.get_right())
                )
                self.play(Write(text_steps[i]))
            elif i <= 2:
                self.play(MoveAlongPath(image_output_cats[i], line_circle, run_time=2))
                self.play(
                    FadeOut(image_output_cats[i], scale=0.1, target_position=self.unet.get_left()),
                    LaggedStart(
                        *[p.animate(rate_func=there_and_back).set_color(TEAL)
                          for prism in self.unet[0] for p in prism],
                        lag_ratio=0.1, run_time=1.5
                    ),
                    FadeTransform(text_steps[i - 1], text_steps[i])
                )
                self.play(FadeIn(image_output_cats[i + 1], scale=0.1, target_position=self.unet.get_right()))
            elif i <= 6:
                self.play(ShowPassingFlash(line_circle.copy().set_color(RED), time_width=1.0, run_time=0.5))
                self.play(
                    LaggedStart(
                        *[p.animate(rate_func=there_and_back).set_color(TEAL)
                          for prism in self.unet[0] for p in prism],
                        lag_ratio=0.1, run_time=0.7
                    ),
                )
                self.play(
                    FadeIn(image_output_cats[i + 1]),
                    FadeTransform(text_steps[i - 1], text_steps[i]),
                    run_time=0.2
                )
            else:
                self.play(
                    FadeIn(image_output_cats[i + 1]),
                    FadeTransform(text_steps[i - 1], text_steps[i]),
                    run_time=0.1
                )
        self.wait()
        self.play(FadeOut(formula_decode, box_decode, arrow_input_model, text_steps[49], no_prompt))
        self.play(Group(self.unet, arrow_model_output, image_output_cats[3:51]).animate.shift(2 * LEFT + 1 * UP))

        image_output_dog.next_to(self.unet, RIGHT, buff=1.0)
        text_question = Text("?").scale(3).next_to(image_output_dog, RIGHT)
        brace_image_set2 = Brace(image_encode_set, direction=UP)
        Group(brace_image_set2, image_encode_set).next_to(self.unet, DOWN)
        self.play(
            FadeIn(image_output_dog, shift=DOWN),
            image_output_cats[3:51].animate.next_to(image_output_dog, DOWN),
            Create(text_question)
        )
        self.play(GrowFromCenter(brace_image_set2), FadeIn(image_encode_set, shift=UP))
        self.play(FadeOut(image_output_dog, self.unet, image_encode_set, brace_image_set2,
                          arrow_model_output, text_question, image_output_cats[3:51]))
        self.wait()

    def clip1(self):
        # 7. show part
        # 还有model_clip
        self.play(FadeTransform(self.title_ddpm, self.title_clip))
        text_encoder = VGroup(self.gear.copy().scale(0.4).set_color(BLUE_C),
                              Text("Text Encoder").scale(0.7)).arrange(RIGHT, buff=0.5)
        image_encoder = VGroup(self.gear.copy().scale(0.4).set_color(BLUE_E),
                               Text("Image Encoder").scale(0.7)).arrange(RIGHT, buff=0.5)
        encoders = VGroup(text_encoder, image_encoder).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        brace_clip = Brace(encoders, direction=LEFT, buff=0.5)
        VGroup(self.model_clip, brace_clip, encoders).arrange(RIGHT, buff=0.7)

        self.play(GrowFromCenter(self.model_clip))
        self.play(GrowFromCenter(brace_clip))
        self.play(
            Indicate(self.model_clip[0][0]),
            TransformFromCopy(self.model_clip[0][0], text_encoder, path_arc=30 * DEGREES)
        )
        self.play(
            Indicate(self.model_clip[0][1]),
            TransformFromCopy(self.model_clip[0][1], image_encoder, path_arc=-30 * DEGREES)
        )
        self.play(FadeOut(brace_clip, encoders))
        self.play(self.model_clip.animate.move_to(2 * LEFT))

        self.wait()

    def clip2(self):
        # 8. clip demo show 3D vector
        # 清理干净
        input_pos = 5 * LEFT
        output_pos = 0.5 * RIGHT
        last_pos = 5 * RIGHT + 1.3 * UP

        text_cat = Text("A CAT").scale(0.9)
        surrounding_text_cat = SurroundingRectangle(
            text_cat, buff=0.1, color=WHITE, corner_radius=0.1, stroke_width=0.7)
        text_cat = VGroup(text_cat, surrounding_text_cat).move_to(input_pos)  #
        embedding_text_cat = WeightMatrix(length=14).set(width=0.5).move_to(output_pos)  #
        brace_text = Brace(embedding_text_cat, direction=RIGHT, buff=0.1)
        dim_text = Text("768-dimensional", font_size=24).set_color(YELLOW_E).next_to(brace_text, RIGHT)
        embedding_text_cat.generate_target()
        embedding_text_cat.target.set(width=0.4).move_to(last_pos)  #
        text_cat.generate_target()
        text_cat.target.set(width=0.45).next_to(embedding_text_cat.target, 1.5 * UP)

        image_cat = ImageMobject("assets/cat.jpg").set(height=2).move_to(input_pos)
        embedding_image_cat = WeightMatrix(length=14).set(width=0.5).move_to(output_pos)
        embedding_image_cat.generate_target()
        embedding_image_cat.target.set(width=0.4).move_to(last_pos + 0.6 * LEFT)
        image_cat.generate_target()
        image_cat.target.set(width=0.45).next_to(embedding_image_cat.target, UP)

        text_dog = Text("A DOG").scale(0.9)
        surrounding_text_dog = SurroundingRectangle(
            text_dog, buff=0.1, color=WHITE, corner_radius=0.1, stroke_width=0.7)
        text_dog = VGroup(text_dog, surrounding_text_dog).move_to(input_pos)
        embedding_text_dog = WeightMatrix(length=14).set(width=0.5).move_to(output_pos)
        embedding_text_dog.generate_target()
        embedding_text_dog.target.set(width=0.4).move_to(last_pos + 1.2 * LEFT)
        text_dog.generate_target()
        text_dog.target.set(width=0.45).next_to(embedding_text_dog.target, 1.5 * UP)

        image_dog = ImageMobject("assets/dog.jpg").set(height=2).move_to(input_pos)
        embedding_image_dog = WeightMatrix(length=14).set(width=0.5).move_to(output_pos)
        embedding_image_dog.generate_target()
        embedding_image_dog.target.set(width=0.4).move_to(last_pos + 1.8 * LEFT)
        image_dog.generate_target()
        image_dog.target.set(width=0.45).next_to(embedding_image_dog.target, UP)

        self.play(Create(text_cat))
        self.play(
            AnimationGroup(
                Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                       about_point=self.gears_clip[i].get_center())
                for i in range(2)
            ),
            LaggedStart(bake_mobject_into_vector_entries(text_cat, embedding_text_cat)),
            run_time=3
        )
        self.play(GrowFromCenter(brace_text), Create(dim_text))
        self.play(FadeOut(brace_text, dim_text))
        self.play(MoveToTarget(embedding_text_cat), MoveToTarget(text_cat))

        self.play(FadeIn(image_cat))
        self.play(
            AnimationGroup(
                Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                       about_point=self.gears_clip[i].get_center())
                for i in range(2)
            ),
            LaggedStart(bake_mobject_into_vector_entries(image_cat, embedding_image_cat, path_arc=-30 * DEGREES)),
            run_time=3
        )
        self.play(GrowFromCenter(brace_text), Create(dim_text))
        self.play(FadeOut(brace_text, dim_text))
        self.play(MoveToTarget(embedding_image_cat), MoveToTarget(image_cat))

        self.play(Create(text_dog))
        self.play(
            AnimationGroup(
                Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                       about_point=self.gears_clip[i].get_center())
                for i in range(2)
            ),
            LaggedStart(bake_mobject_into_vector_entries(text_dog, embedding_text_dog)), run_time=3
        )
        self.play(MoveToTarget(embedding_text_dog), MoveToTarget(text_dog))

        self.play(FadeIn(image_dog))
        self.play(
            AnimationGroup(
                Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                       about_point=self.gears_clip[i].get_center())
                for i in range(2)
            ),
            LaggedStart(bake_mobject_into_vector_entries(image_dog, embedding_image_dog, path_arc=-30 * DEGREES)),
            run_time=3
        )
        self.play(MoveToTarget(embedding_image_dog), MoveToTarget(image_dog))
        self.wait()

        # 9. 3D show
        axes = ThreeDAxes()
        arrow_text_dog = ArrowWithLabel(
            axes.get_origin(),
            [3, 2, 2],
            stroke_width=2.0,
            stroke_color=BLUE,
            label=Text('dog text', font_size=14),
            buff=0,
        )
        arrow_image_dog = ArrowWithLabel(
            axes.get_origin(),
            [1, 3, 1.8],
            stroke_width=2.0,
            stroke_color=BLUE,
            label=Text('dog image', font_size=14),
            buff=0,
        )

        arrow_text_cat = ArrowWithLabel(
            axes.get_origin(),
            [-2, -1, 2],
            stroke_width=2.0,
            stroke_color=RED,
            label=Text('cat text', font_size=14),
            buff=0,
        )
        arrow_image_cat = ArrowWithLabel(
            axes.get_origin(),
            [-1.5, -2, 2.5],
            stroke_width=2.0,
            stroke_color=RED,
            label=Text('cat image', font_size=14),
            buff=0,
        )

        self.play(FadeOut(self.model_clip))
        self.add_fixed_in_frame_mobjects(
            embedding_image_dog, image_dog,
            embedding_text_dog, text_dog,
            embedding_image_cat, image_cat,
            embedding_text_cat, text_cat, self.title_clip
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes))
        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(
            FadeTransform(embedding_image_dog, arrow_image_dog),
            FadeOut(image_dog),
            FadeIn(arrow_image_dog.label)
        )
        self.play(
            FadeTransform(VGroup(embedding_text_dog, text_dog), arrow_text_dog),
            FadeIn(arrow_text_dog.label)
        )
        self.play(
            FadeTransform(embedding_image_cat, arrow_image_cat),
            FadeOut(image_cat),
            FadeIn(arrow_image_cat.label)
        )
        self.play(
            FadeTransform(VGroup(embedding_text_cat, text_cat), arrow_text_cat),
            FadeIn(arrow_text_cat.label)
        )
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(arrow_image_cat, arrow_text_cat,
                          arrow_image_dog, arrow_text_dog,
                          arrow_text_cat.label, arrow_text_dog.label,
                          arrow_image_dog.label, arrow_image_cat.label
                          ))
        self.play(FadeOut(axes))
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        self.wait()

    def clip3(self):
        # 10. show text encoder
        # 只剩model_clip
        phrase = "a cyberpunk with natural greys and whites and browns"
        words = list(filter(lambda s: s.strip(), phrase.split(" ")))
        text_words = VGroup(*[Text(word).scale(0.4) for word in words])
        text_words.arrange(RIGHT, buff=0.15).move_to(RIGHT + 3 * UP)
        rect_words = VGroup()
        for word in text_words:
            rect = SurroundingRectangle(word, buff=-0.013).set_stroke(GREY, 2).set_fill(GREY, 0.2)
            rect.stretch_to_fit_height(0.45)
            rect.stretch_to_fit_width(rect.width + 0.16)
            rect.align_to(word, RIGHT)
            rect_words.add(rect)
        rect_words.set_submobject_colors_by_gradient(BLUE_C, BLUE_D, GREEN)

        text_numbers = VGroup(*[Text(f"{n}", font="Menlo").scale(0.4).next_to(rect_words[i], DOWN, buff=1.0)
                                for i, n in enumerate([4, 14323, 237, 673, 554, 28, 489, 28, 1921])])
        arrow_numbers = VGroup(*[Arrow(rect_words[i].get_bottom(), text_numbers[i].get_top())
                                 for i in range(len(rect_words))])
        brace_numbers = Brace(VGroup(text_words, text_numbers), direction=LEFT)
        text_tokenizer = Text("Tokenizer").scale(0.5).set_color(YELLOW_E).next_to(brace_numbers, LEFT)

        embedding_words = VGroup(*[WeightMatrix(length=10).set(width=0.5).next_to(rect, DOWN, buff=2.0)
                                   for rect in rect_words])
        arrow_embeds = VGroup(*[Arrow(text_numbers[i].get_bottom(), embedding_words[i].get_top())
                                for i in range(len(rect_words))])

        emb_syms = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}").scale(0.9).next_to(rect, DOWN, buff=0.75).set_color(GREY_A)
                            for n, rect in enumerate(rect_words, start=1)])
        arrow_embeds.target = arrow_embeds.generate_target()
        for rect, arrow, sym in zip(rect_words, arrow_embeds.target, emb_syms):
            low_point = sym.get_top()
            top_point = np.array([low_point[0], rect.get_y(DOWN), 0])
            arrow.become(Arrow(top_point, low_point, buff=SMALL_BUFF))

        box_width = emb_syms.get_right()[0] - emb_syms.get_left()[0] + 1

        box = (Rectangle(width=box_width, height=2.0)
               .set_fill(GREY_E, 1).set_stroke(WHITE, 1).move_to(emb_syms.get_center() + 2 * DOWN))
        text_box = Text("Self-Attention").scale(0.7).move_to(box.get_top() + 0.3 * DOWN)
        attention_box = VGroup(box, text_box)
        box_arrows_in = VGroup(*[Arrow(sym.get_bottom(), np.array([sym.get_bottom()[0], box.get_top()[1], 0]))
                                 for sym in emb_syms])
        emb_syms_copy = emb_syms.copy().move_to(box.get_center() + DOWN)
        emb_sym_primes = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}^{{'}}").scale(0.9).move_to(sym.get_center() + 4 * DOWN)
                                  for n, sym in enumerate(emb_syms, start=1)])
        box_arrows_out = VGroup(*[Arrow(np.array([sym.get_bottom()[0], box.get_bottom()[1], 0]),
                                        np.array([sym.get_bottom()[0], emb_sym_primes[i].get_top()[1], 0]))
                                  for i, sym in enumerate(emb_syms)])
        emb_sym_out = emb_sym_primes[-1].copy()
        rect_out = SurroundingRectangle(emb_sym_out).set_stroke(YELLOW_E, 2)
        emb_sym_out.generate_target()
        emb_sym_out.target.scale(1.4).move_to(np.array([text_words.get_center()[0], -0.5, 0]))
        arrow_embed_out = Arrow(text_words.get_bottom() + 0.5 * DOWN, emb_sym_out.target.get_top() + 0.5 * UP)
        embedding_out = WeightMatrix(length=14).set(width=0.5).move_to(emb_sym_out.target)
        arrow_embed_out.generate_target()
        arrow_embed_out.target = Arrow(text_words.get_bottom(), embedding_out.get_top())
        brace_text = Brace(embedding_out, direction=RIGHT, buff=0.1)
        dim_text = Text("768-dimensional").scale(0.5).set_color(YELLOW_E).next_to(brace_text, RIGHT)
        self.model_clip.move_to(5 * LEFT)

        self.play(GrowFromCenter(self.model_clip))
        self.play(LaggedStartMap(FadeIn, text_words, shift=0.5 * UP, lag_ratio=0.25))
        self.play(LaggedStartMap(DrawBorderThenFill, rect_words))
        self.play(
            LaggedStartMap(GrowArrow, arrow_numbers),
            LaggedStartMap(Create, text_numbers)
        )
        self.play(GrowFromCenter(brace_numbers), Write(text_tokenizer))
        self.play(
            LaggedStartMap(GrowArrow, arrow_embeds),
            LaggedStartMap(FadeIn, embedding_words, shift=0.5 * DOWN)
        )
        self.play(
            FadeOut(arrow_numbers, text_numbers, brace_numbers, text_tokenizer),
            LaggedStart(*[Transform(embed, sym)
                          for sym, embed in zip(emb_syms, embedding_words)],
                        group_type=Group,
                        run_time=2
                        ),
            LaggedStartMap(FadeIn, emb_syms, shift=UP),
            MoveToTarget(arrow_embeds, lag_ratio=0.1, run_time=2)
        )
        self.play(
            LaggedStartMap(GrowArrow, box_arrows_in),
            Create(attention_box)
        )
        self.play(
            LaggedStart(
                AnimationGroup(
                    *[ContextAnimation(target, emb_syms_copy,
                                       time_width=2, max_stroke_width=5, lag_ratio=0.2, path_arc=70 * DEGREES)
                      for target in emb_syms_copy])
            ), lag_ratio=0.2
        )
        self.play(
            LaggedStartMap(GrowArrow, box_arrows_out),
            LaggedStartMap(FadeIn, emb_sym_primes, shift=DOWN)
        )
        self.play(Create(rect_out))
        self.play(
            FadeOut(attention_box, box_arrows_in, box_arrows_out, emb_sym_primes,
                    emb_syms, arrow_embeds, rect_out, embedding_words),
            MoveToTarget(emb_sym_out),
            GrowArrow(arrow_embed_out))
        self.play(
            Transform(emb_sym_out, embedding_out),
            MoveToTarget(arrow_embed_out)
        )
        self.play(GrowFromCenter(brace_text), Create(dim_text))
        self.play(FadeOut(brace_text, dim_text))
        self.play(FadeOut(emb_sym_out, arrow_embed_out, text_words, rect_words))

        self.wait()

    def clip4(self):
        # 11. show image encoder
        # 只剩model_clip
        image_prompt = Image.open("assets/prompt.png")
        img_width, img_height = image_prompt.size
        num_width, num_height = 3, 3
        sub_images = []
        sub_width = img_width // num_width
        sub_height = img_height // num_height
        for i in range(num_height):
            for j in range(num_width):
                left = j * sub_width
                upper = i * sub_height
                right = (j + 1) * sub_width
                lower = (i + 1) * sub_height
                sub_image = image_prompt.crop((left, upper, right, lower))
                sub_images.append(sub_image)

        image_grid = Group(*[
            Group(*[ImageMobject(np.array(sub_images[num_height * i + j])).scale(0.5)
                    for j in range(num_width)]).arrange(RIGHT, buff=0.0)
            for i in range(num_height)
        ]).arrange(DOWN, buff=0.0)
        image_grid.generate_target()
        image_grid.target = Group(*[
            Group(*[ImageMobject(np.array(sub_images[num_height * i + j])).scale(0.5)
                    for j in range(num_width)]).arrange(RIGHT, buff=0.12)
            for i in range(num_height)
        ]).arrange(DOWN, buff=0.12)

        self.play(FadeIn(image_grid))
        self.play(MoveToTarget(image_grid))
        self.wait()

        image_grid.generate_target()
        image_grid.target = Group(*[
            Group(*[ImageMobject(np.array(sub_images[num_height * i + j])).scale(0.5)
                    for j in range(num_width)]).arrange(RIGHT, buff=0.12)
            for i in range(num_height)
        ]).arrange(RIGHT, buff=0.12).move_to(3 * UP + RIGHT).scale(0.7)
        self.play(MoveToTarget(image_grid))
        self.wait()

        image_grid = Group(*[j for image_grid_line in image_grid for j in image_grid_line])
        image_embedding_words = VGroup(*[WeightMatrix(length=10).set(width=0.5).next_to(im, DOWN, buff=1.0)
                                         for im in image_grid])
        image_arrow_embeds = VGroup(*[Arrow(image_grid[i].get_bottom(), image_embedding_words[i].get_top())
                                      for i in range(len(image_grid))])

        image_emb_syms = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}").scale(0.9)
                                .next_to(im, DOWN, buff=0.75).set_color(GREY_A)
                                  for n, im in enumerate(image_grid, start=1)])
        image_arrow_embeds.generate_target()
        for i, arrow in enumerate(image_arrow_embeds.target):
            arrow.become(Arrow(image_grid[i].get_bottom(), image_emb_syms[i].get_top(), buff=SMALL_BUFF))
        box_width = image_emb_syms.get_right()[0] - image_emb_syms.get_left()[0] + 1

        box = (Rectangle(width=box_width, height=2.0)
               .set_fill(GREY_E, 1).set_stroke(WHITE, 1).move_to(image_emb_syms.get_center() + 2 * DOWN))
        text_box = Text("Self-Attention").scale(0.7).move_to(box.get_top() + 0.3 * DOWN)
        attention_box = VGroup(box, text_box)
        box_arrows_in = VGroup(*[Arrow(sym.get_bottom(), np.array([sym.get_bottom()[0], box.get_top()[1], 0]))
                                 for sym in image_emb_syms])
        emb_syms_copy = image_emb_syms.copy().move_to(box.get_center() + DOWN)
        emb_sym_primes = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}^{{'}}").scale(0.9).move_to(sym.get_center() + 4 * DOWN)
                                  for n, sym in enumerate(image_emb_syms, start=1)])
        box_arrows_out = VGroup(*[Arrow(np.array([sym.get_bottom()[0], box.get_bottom()[1], 0]),
                                        np.array([sym.get_bottom()[0], emb_sym_primes[i].get_top()[1], 0]))
                                  for i, sym in enumerate(image_emb_syms)])
        emb_sym_out = emb_sym_primes[-1].copy()
        rect_out = SurroundingRectangle(emb_sym_out).set_stroke(YELLOW_E, 2)
        emb_sym_out.generate_target()
        emb_sym_out.target.scale(1.4).move_to(np.array([image_grid.get_center()[0], -0.5, 0]))
        arrow_embed_out = Arrow(image_grid.get_bottom() + 0.5 * DOWN, emb_sym_out.target.get_top() + 0.5 * UP)
        embedding_out = WeightMatrix(length=14).set(width=0.5).move_to(emb_sym_out.target)
        arrow_embed_out.generate_target()
        arrow_embed_out.target = Arrow(image_grid.get_bottom(), embedding_out.get_top())

        self.play(
            LaggedStartMap(GrowArrow, image_arrow_embeds),
            LaggedStartMap(FadeIn, image_embedding_words, shift=0.5 * DOWN)
        )
        self.play(
            LaggedStart(*[Transform(embed, sym)
                          for sym, embed in zip(image_emb_syms, image_embedding_words)],
                        group_type=Group,
                        run_time=2
                        ),
            LaggedStartMap(FadeIn, image_emb_syms, shift=UP),
            MoveToTarget(image_arrow_embeds, lag_ratio=0.1, run_time=2)
        )
        self.play(
            LaggedStartMap(GrowArrow, box_arrows_in),
            Create(attention_box)
        )
        self.play(
            LaggedStart(
                AnimationGroup(
                    *[ContextAnimation(target, emb_syms_copy,
                                       time_width=2, max_stroke_width=5, lag_ratio=0.2, path_arc=70 * DEGREES)
                      for target in emb_syms_copy])
            ), lag_ratio=0.2
        )
        self.play(
            LaggedStartMap(GrowArrow, box_arrows_out),
            LaggedStartMap(FadeIn, emb_sym_primes, shift=DOWN)
        )
        self.play(Create(rect_out))
        self.play(
            FadeOut(attention_box, box_arrows_in, box_arrows_out, emb_sym_primes,
                    image_emb_syms, image_arrow_embeds, rect_out, image_embedding_words),
            MoveToTarget(emb_sym_out),
            GrowArrow(arrow_embed_out)
        )
        self.play(
            Transform(emb_sym_out, embedding_out),
            MoveToTarget(arrow_embed_out)
        )
        self.play(FadeOut(emb_sym_out, arrow_embed_out, image_grid))
        self.wait()

    def clip5(self):
        # 12. explain how CLIP works
        self.model_text_encoder.move_to(2.5 * LEFT + 2.5 * UP)
        self.model_image_encoder.move_to(2.5 * LEFT + 1.5 * DOWN)

        text_set = Group(
            Text("A CAT").set(width=2).set_opacity(1.0),
            Text("A CAT").set(width=2).set_opacity(0.4).shift(0.1 * UP + 0.1 * RIGHT),
            Text("A CAT").set(width=2).set_opacity(0.3).shift(0.2 * UP + 0.2 * RIGHT),
            Text("A CAT").set(width=2).set_opacity(0.2).shift(0.3 * UP + 0.3 * RIGHT),
            Text("A CAT").set(width=2).set_opacity(0.1).shift(0.4 * UP + 0.4 * RIGHT),
            Text("A CAT").set(width=2).set_opacity(0.05).shift(0.5 * UP + 0.5 * RIGHT),
        ).move_to(5.5 * LEFT + 2.5 * UP)

        image_set = Group(
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(1.0),
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(0.4).shift(0.1 * UP + 0.1 * RIGHT),
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(0.3).shift(0.2 * UP + 0.2 * RIGHT),
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(0.2).shift(0.3 * UP + 0.3 * RIGHT),
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(0.1).shift(0.4 * UP + 0.4 * RIGHT),
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(0.05).shift(0.5 * UP + 0.5 * RIGHT),
        ).move_to(5.5 * LEFT + 1.5 * DOWN)

        # lines
        table_mid = 3.5 * RIGHT + 1.5 * DOWN
        grid_size = 0.75
        grid_num = 6
        table = Rectangle(
            width=grid_size * grid_num,
            height=grid_size * grid_num,
            grid_xstep=grid_size,
            grid_ystep=grid_size,
        ).set_stroke(width=2.0, color=GREY).move_to(table_mid)
        table_text = Rectangle(
            width=grid_size * grid_num,
            height=grid_size,
            grid_xstep=grid_size,
        ).set_stroke(width=2.0, color=GREY).next_to(table, UP, buff=0.3)
        table_image = Rectangle(
            width=grid_size,
            height=grid_size * grid_num,
            grid_ystep=grid_size,
        ).set_stroke(width=2.0, color=GREY).next_to(table, LEFT, buff=0.3)
        lines_out_image = VGroup(*[
            CubicBezier(
                self.model_image_encoder.get_right(),
                self.model_image_encoder.get_right() + 1.0 * RIGHT,
                table_image.get_left() + (2.5 * UP + i * DOWN) * grid_size + 1.0 * LEFT,
                table_image.get_left() + (2.5 * UP + i * DOWN) * grid_size,
                stroke_width=2.0
            ) for i in range(grid_num)])
        lines_out_image.set_submobject_colors_by_gradient(TEAL, BLUE_E)

        lines_out_text = VGroup(*[
            CubicBezier(
                self.model_text_encoder.get_right(),
                table_text.get_top() + (2.5 * LEFT + i * RIGHT) * grid_size + 0.7 * UP,
                table_text.get_top() + (2.5 * LEFT + i * RIGHT) * grid_size + 0.6 * UP,
                table_text.get_top() + (2.5 * LEFT + i * RIGHT) * grid_size,
                stroke_width=2.0
            ) for i in range(grid_num)])
        lines_out_text.set_submobject_colors_by_gradient(TEAL, BLUE_E)

        syms_text = VGroup(
            *[MathTex(f"T_{{{i}}}")
              .set(width=grid_size - 0.45)
              .set_color(GREY)
              .move_to(table_text.get_center() + (3.5 * LEFT + i * RIGHT) * grid_size)
              for i in range(1, grid_num + 1)]
        )

        syms_image = VGroup(
            *[MathTex(f"I_{{{i}}}")
              .set(width=grid_size - 0.45)
              .set_color(GREY)
              .move_to(table_image.get_center() + (3.5 * UP + i * DOWN) * grid_size)
              for i in range(1, grid_num + 1)]
        )

        syms_image_text = VGroup(
            *[MathTex(f"I_{{{i}}}", f"\cdot ", f"T_{{{j}}}")
              .set(width=grid_size - 0.2)
              .set_color(GREY)
              .move_to(table_mid + (3.5 * UP + i * DOWN + 3.5 * LEFT + j * RIGHT) * grid_size)
              for j in range(1, grid_num + 1) for i in range(1, grid_num + 1)]
        )

        circle_image_text = VGroup(
            *[Circle(
                radius=random.uniform(0.15, 0.25) if j == i else random.uniform(0.05, 0.1),
                fill_color=GREY, fill_opacity=0.8, stroke_width=0.0
            ).move_to(table_mid + (2.5 * UP + i * DOWN + 2.5 * LEFT + j * RIGHT) * grid_size)
              for j in range(grid_num) for i in range(grid_num)]
        )

        loss_func = MathTex(
            r"\operatorname{loss}=",
            r"-\frac{1}{2|\mathcal{B}|} ",
            r"\sum_{i=1}^{|\mathcal{B}|}\left(",
            r"\log \frac{e^{t \mathbf{x}_i \cdot \mathbf{y}_i}}{\sum_{j=1}^{|\mathcal{B}|} e^{t \mathbf{x}_i \cdot \mathbf{y}_j}}",
            r"+",
            r"\log \frac{e^{t \mathbf{x}_i \cdot \mathbf{y}_i}}{\sum_{j=1}^{|\mathcal{B}|} e^{t \mathbf{x}_j \cdot \mathbf{y}_i}}",
            r"\right)"
        )
        loss_func.move_to(3.5 * LEFT + 0.5 * UP).scale(0.5)
        loss_func_box1 = SurroundingRectangle(
            loss_func[3], buff=0.05, corner_radius=0.01, stroke_width=2.0, stroke_color=YELLOW_E
        )
        loss_func_box2 = SurroundingRectangle(
            loss_func[5], buff=0.05, corner_radius=0.01, stroke_width=2.0, stroke_color=YELLOW_E
        )
        table_box1 = SurroundingRectangle(
            table_text.copy().move_to(table.get_top() + grid_size / 2 * DOWN),
            buff=0.1, corner_radius=0.1, stroke_width=2.0, stroke_color=YELLOW_E
        )
        table_box2 = SurroundingRectangle(
            table_image.copy().move_to(table.get_left() + grid_size / 2 * RIGHT),
            buff=0.1, corner_radius=0.1, stroke_width=2.0, stroke_color=YELLOW_E
        )
        arrow_1 = Arrow(
            table_box1.get_top(), loss_func_box1.get_top(),
            path_arc=30 * DEGREES, buff=0.1,
            stroke_width=2.5, tip_length=0.15,
            max_tip_length_to_length_ratio=1.0,
            max_stroke_width_to_length_ratio=20
        )
        arrow_2 = Arrow(
            table_box2.get_left(), loss_func_box2.get_bottom(),
            path_arc=-30 * DEGREES, buff=0.1,
            stroke_width=2.5, tip_length=0.15,
            max_tip_length_to_length_ratio=1.0,
            max_stroke_width_to_length_ratio=20
        )

        self.play(
            Indicate(self.model_clip[0][0]),
            TransformFromCopy(self.model_clip[0][0], self.model_text_encoder, path_arc=30 * DEGREES)
        )
        self.play(
            Indicate(self.model_clip[0][1]),
            TransformFromCopy(self.model_clip[0][1], self.model_image_encoder, path_arc=-30 * DEGREES)
        )
        self.play(FadeOut(self.model_clip, shift=LEFT))
        self.play(LaggedStartMap(FadeIn, text_set, shift=DOWN, path_arc=30 * DEGREES, lag_ratio=0.1))
        self.play(LaggedStartMap(FadeIn, image_set, shift=DOWN, path_arc=30 * DEGREES, lag_ratio=0.1))
        self.play(FadeIn(table_text), Create(lines_out_text))
        self.play(
            LaggedStart(*[FadeOut(tx, target_position=sym.get_center(), path_arc=30 * DEGREES)
                          for tx, sym in zip(text_set.copy(), syms_text)],
                        lag_ratio=0.05,
                        run_time=2,
                        remover=True
                        ),
            LaggedStartMap(ShowPassingFlash, lines_out_text.copy().set_color(RED),
                           lag_ratio=5e-3,
                           time_width=0.5,
                           run_time=2
                           ),
            LaggedStartMap(Write, syms_text,
                           lag_ratio=0.1,
                           run_time=3
                           ),
        )
        self.play(FadeIn(table_image), Create(lines_out_image))
        self.play(
            LaggedStart(*[FadeOut(tx, target_position=sym.get_center(), path_arc=30 * DEGREES)
                          for tx, sym in zip(image_set.copy(), syms_image)],
                        lag_ratio=0.05,
                        run_time=2,
                        remover=True
                        ),
            LaggedStartMap(ShowPassingFlash, lines_out_image.copy().set_color(RED),
                           lag_ratio=5e-3,
                           time_width=0.5,
                           run_time=2
                           ),
            LaggedStartMap(Write, syms_image,
                           lag_ratio=0.1,
                           run_time=3
                           ),
        )
        self.play(FadeIn(table))
        self.add(syms_image_text)
        self.play(
            LaggedStart(
                *[LaggedStart(
                    *[TransformFromCopy(syms_text[i], syms_image_text[grid_num * i + j][2], path_arc=30 * DEGREES)
                      for j in range(grid_num)],
                    lag_ratio=0.1
                ) for i in range(grid_num)],
                lag_ratio=0.1,
                run_time=4
            ),
            LaggedStart(
                *[LaggedStart(
                    *[TransformFromCopy(syms_image[i], syms_image_text[grid_num * i + j][0], path_arc=-30 * DEGREES)
                      for j in range(grid_num)],
                    lag_ratio=0.1
                ) for i in range(grid_num)],
                lag_ratio=0.1,
                run_time=4
            ),
        )
        self.play(
            syms_image_text.animate.set_opacity(0.3),
            FadeIn(circle_image_text)
        )
        self.play(Write(loss_func))
        self.play(Create(loss_func_box1), Create(table_box1))
        self.play(GrowArrow(arrow_1))
        self.play(Create(loss_func_box2), Create(table_box2))
        self.play(GrowArrow(arrow_2))
        self.play(FadeOut(loss_func_box1, table_box1, arrow_1, loss_func_box2, table_box2, arrow_2,
                          syms_image_text, table, table_text, syms_text, table_image, syms_image,
                          lines_out_text, lines_out_image, circle_image_text, loss_func, text_set, image_set,
                          self.model_image_encoder, self.model_text_encoder))
        self.wait()

    def clip6(self):
        bert = ImageMobject("assets/bert.png").set(width=2.5).move_to(5 * LEFT)
        text_bert = Text("Does Bert work?").scale(1.1).move_to(2.5 * UP)
        image_cat_glasses = ImageMobject("assets/cat_glasses.jpg").set(width=4.0).next_to(text_bert, DOWN, buff=0.7)
        text_cat_glasses = Text("a cat with glasses").scale(0.5).next_to(image_cat_glasses, DOWN, buff=0.2)
        text_answer = Text("No!").next_to(text_bert, RIGHT, buff=1.0)
        box = SurroundingRectangle(text_cat_glasses[8:],
                                   color=YELLOW_E, buff=0.05, corner_radius=0.05, stroke_width=1.5)

        self.add(bert, text_bert, image_cat_glasses, text_cat_glasses, text_answer, box)

    def latent1(self):
        training_data = Group(
            Group(
                ImageMobject("assets/cat.jpg").set(width=3.0),
                Text("a photo of a cat", font='Menlo').scale(0.3)
            ).arrange(DOWN, buff=0.05),
            Group(
                ImageMobject("assets/dog.jpg").set(width=3.0),
                Text("a photo of a dog", font='Menlo').scale(0.3)
            ).arrange(DOWN, buff=0.05),
            Group(
                ImageMobject("assets/cat_glasses.jpg").set(width=3.0),
                Text("a cat with glasses", font='Menlo').scale(0.3)
            ).arrange(DOWN, buff=0.05),
            Text("···")
        ).arrange(RIGHT, buff=0.3)
        image_cat = training_data[0][0].copy()
        image_cat.generate_target()
        image_cat.target.set(width=4.5).move_to(ORIGIN)
        brace_image_up = Brace(image_cat.target, UP, buff=0.2)
        text_pixel1 = Text("1024 pixels", font_size=36).next_to(brace_image_up, UP)
        brace_image_right = Brace(image_cat.target, RIGHT, buff=0.2)
        text_pixel2 = Text("1024 pixels", font_size=36).next_to(brace_image_right, RIGHT)

        self.play(LaggedStartMap(FadeIn, training_data, lag_ratio=0.5, shift=DOWN))
        self.play(FadeOut(training_data), MoveToTarget(image_cat))
        self.play(GrowFromCenter(brace_image_up), Write(text_pixel1))
        self.play(GrowFromCenter(brace_image_right), Write(text_pixel2))

        # --------------------------------------------------
        image_big = Group(image_cat, brace_image_up, text_pixel1)
        image_big.generate_target()
        image_cat_blurred = ImageMobject("assets/cat_blurred.jpg").set(width=2.0)
        small_brace_image_up = Brace(image_cat_blurred, UP, buff=0.2)
        small_text_pixel1 = Text("64 pixels", font_size=20).next_to(small_brace_image_up, UP)
        small_brace_image_right = Brace(image_cat_blurred, RIGHT, buff=0.2)
        small_text_pixel2 = Text("64 pixels", font_size=20).next_to(small_brace_image_right, RIGHT)
        image_small = Group(image_cat_blurred, small_brace_image_up, small_text_pixel1,
                            small_brace_image_right, small_text_pixel2)
        Group(image_big.target, image_small).arrange(RIGHT, buff=1.0)

        self.play(
            FadeOut(brace_image_right, text_pixel2),
            MoveToTarget(image_big),
            FadeIn(image_small)
        )
        self.play(FadeOut(image_big, image_small))

        # --------------------------------------------------
        self.model_vqvae.move_to(2 * UP)
        matrix_image = VGroup(
            WeightMatrix(shape=(14, 8)).set(width=2),
            WeightMatrix(shape=(14, 8)).set(width=2).set_opacity(0.3).shift(0.1 * RIGHT + 0.1 * UP),
            WeightMatrix(shape=(14, 8)).set(width=2).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP),
            WeightMatrix(shape=(14, 8)).set(width=2).set_opacity(0.1).shift(0.3 * RIGHT + 0.3 * UP),
        )
        image_cat.set(width=3)
        image_cat_copy = image_cat.copy()
        model_and_image = Group(
            image_cat, self.model_vae_encoder,
            matrix_image, self.model_vae_decoder, image_cat_copy
        ).arrange(RIGHT, buff=0.6).shift(DOWN)

        brace_matrix1 = BraceBetweenPoints(matrix_image[3].get_corner(UL),
                                           matrix_image[0].get_corner(UL), buff=0.1, color=GREY)
        text_dim1 = Text("4").scale(0.4).next_to(brace_matrix1, LEFT)
        brace_matrix2 = Brace(matrix_image[0], direction=RIGHT, buff=0.1, color=GREY)
        text_dim2 = Text("64").scale(0.4).next_to(brace_matrix2, RIGHT, buff=0.1)
        brace_matrix3 = Brace(matrix_image[0], direction=DOWN, buff=0.1, color=GREY)
        text_dim3 = Text("64").scale(0.4).next_to(brace_matrix3, DOWN, buff=0.1)

        self.play(FadeIn(self.model_vqvae, shift=DOWN))
        self.play(
            Indicate(self.model_vqvae[0][0]),
            TransformFromCopy(self.model_vqvae[0][0], self.model_vae_encoder, path_arc=30 * DEGREES)
        )
        self.play(
            Indicate(self.model_vqvae[0][1]),
            TransformFromCopy(self.model_vqvae[0][1], self.model_vae_decoder, path_arc=-30 * DEGREES)
        )
        self.play(FadeIn(image_cat, shift=DOWN))
        self.play(
            Rotate(self.gears_vae_encoder[0], axis=IN,
                   about_point=self.gears_vae_encoder[0].get_center()),
            Create(matrix_image)
        )
        self.play(
            GrowFromCenter(brace_matrix1), Write(text_dim1),
            GrowFromCenter(brace_matrix2), Write(text_dim2),
            GrowFromCenter(brace_matrix3), Write(text_dim3)
        )
        self.play(
            Rotate(self.gears_vae_decoder[0], axis=IN,
                   about_point=self.gears_vae_decoder[0].get_center()),
            FadeIn(image_cat_copy, shift=DOWN)
        )
        self.play(
            FadeOut(model_and_image, brace_matrix1, brace_matrix2, brace_matrix3,
                    text_dim1, text_dim2, text_dim3, self.model_vqvae)
        )

        # --------------------------------------------------
        training_data.scale(0.7).to_edge(UP)
        model_embedding = Group(
            self.model_vae_encoder.set(height=1),
            self.model_text_encoder.set(height=1)
        ).arrange(RIGHT, buff=2.0).next_to(training_data, DOWN, buff=0.3)
        list_matrix = [
            Group(
                VGroup(
                    WeightMatrix(shape=(13, 8)).set(width=2),
                    WeightMatrix(shape=(13, 8)).set(width=2).set_opacity(0.3).shift(0.1 * RIGHT + 0.1 * UP),
                    WeightMatrix(shape=(13, 8)).set(width=2).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP),
                    WeightMatrix(shape=(13, 8)).set(width=2).set_opacity(0.1).shift(0.3 * RIGHT + 0.3 * UP),
                ),
                WeightMatrix(length=15).set(width=0.4)
            ).arrange(RIGHT, buff=0.02) for i in range(3)]
        list_matrix.append(Text("···"))
        training_data_embedding = Group(*list_matrix).arrange(RIGHT, buff=0.7).next_to(model_embedding, DOWN, buff=0.5)

        self.play(FadeIn(training_data, shift=DOWN))
        self.play(FadeIn(model_embedding, shift=RIGHT))
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        FadeOut(training_data[i].copy(), scale=0.1, target_position=training_data_embedding[i]),
                        FadeIn(training_data_embedding[i], shift=UP)
                    )
                    for i in range(4)
                ],
                lag_ratio=0.5
            ),
            Rotate(self.gears_vae_encoder[0], axis=IN,
                   about_point=self.gears_vae_encoder[0].get_center()),
            Rotate(self.gears_text_encoder[0], axis=IN,
                   about_point=self.gears_text_encoder[0].get_center()),
            run_time=3
        )
        # --------------------------------------------------
        self.play(
            FadeOut(training_data, model_embedding),
            training_data_embedding.animate.to_edge(UP, buff=0.5)
        )
        brace_embedding = Brace(training_data_embedding, DOWN, color=GREY)
        formula_encode = MathTex(
            r"\operatorname{loss}=|\boldsymbol{\epsilon}-",
            r"\boldsymbol{\epsilon}_\theta",
            r"(\mathbf{x}_t, t)\|^2"
        ).scale(0.7).next_to(brace_embedding, DOWN, buff=0.2)
        self.unet.next_to(formula_encode, DOWN, buff=0.5)
        self.play(GrowFromCenter(brace_embedding), Write(formula_encode))
        self.play(FadeIn(self.unet, shift=RIGHT))
        self.play(
            FadeOut(brace_embedding, formula_encode, training_data_embedding),
            self.unet.animate.move_to(ORIGIN)
        )
        self.wait()

    def latent2(self):
        self.unet.move_to(ORIGIN)
        noise = SVGMobject("assets/prism0.svg").move_to(3.8 * LEFT + 0.7 * UP)
        noise_out = SVGMobject("assets/prism0.svg").move_to(3.8 * RIGHT + 0.7 * UP)
        self.model_text_encoder.move_to(5.5 * LEFT + 1.5 * DOWN)
        self.model_vae_decoder.move_to(5.3 * RIGHT + 0.7 * UP)
        self.prompt.scale(0.6).next_to(self.model_text_encoder, DOWN, buff=0.5)
        embedding_prompt = WeightMatrix(length=15).set(width=0.3).next_to(self.model_text_encoder, RIGHT, buff=0.5)
        image_prompt = ImageMobject("assets/prompt.png").set(width=2.0).next_to(self.model_vae_decoder, DOWN, buff=0.5)
        text_steps = VGroup(
            *[Text(f"Step {i + 1}", color=GREY).scale(0.6).next_to(self.unet, UP, buff=1.0)
              for i in range(50)
              ]
        )
        text_dim1 = Text("4 * 64 * 64", color=GREY, font='Menlo').scale(0.3).next_to(noise, LEFT)
        text_dim2 = Text("4 * 64 * 64", color=GREY, font='Menlo').scale(0.3).next_to(noise_out, UP)
        arrow_out_decode = Arrow(noise_out.get_center(),
                                 self.model_vae_decoder.get_left(),
                                 stroke_width=2.0, tip_length=0.15, color=GREY, buff=0.05)
        arrow_decode_image = Arrow(self.model_vae_decoder.get_bottom(),
                                   image_prompt.get_top(),
                                   stroke_width=2.0, tip_length=0.15, color=GREY, buff=0.05)
        arrow_embedding = Arrow(embedding_prompt.get_right() + 0.2 * LEFT,
                                embedding_prompt.get_right() + 7.5 * RIGHT,
                                color=GREY, stroke_width=2.0, tip_length=0.2)
        line_embedding = Line(embedding_prompt.get_right() + 0.2 * LEFT,
                              embedding_prompt.get_right() + 7 * RIGHT).set_stroke(RED, 5.0)
        arrow_prompt_encode = Arrow(self.prompt.get_top(),
                                    self.model_text_encoder.get_bottom(),
                                    color=GREY, stroke_width=2.0, tip_length=0.2, buff=0.05)
        arrow_encode_embed = Arrow(self.model_text_encoder.get_right(),
                                   embedding_prompt.get_left(),
                                   color=GREY, stroke_width=2.0, tip_length=0.2, buff=0.05)
        line_circle = CubicBezier(
            noise_out.get_center(),
            noise_out.get_center() + 2.5 * UP,
            noise.get_center() + 2.5 * UP,
            noise.get_center()
        ).set_stroke(GREY, 2.0)

        rate_list = [0.75, 0.5, 0.3, 1 / 9, 0.3, 0.5, 0.75]
        delta = 0.1
        line_embedding_unet = VGroup()
        for i, prisms in enumerate(self.unet[0]):
            for p in prisms:
                p_end = (p.get_left() - p.get_center()) * rate_list[i] + p.get_bottom()
                p_start = (p_end[0] - delta) * RIGHT + arrow_embedding.get_right()[1] * UP
                line_embedding_unet.add(Line(p_start, p_end, color=GREY, stroke_width=2.0))

        # self.add(
        #     self.unet, self.prompt, self.model_text_encoder, self.model_vae_decoder,
        #     embedding_prompt, arrow_embedding, line_embedding_unet, text_scheduler, image_prompt,
        #     noise, noise_out, arrow_out_decode, arrow_decode_image,
        #     arrow_prompt_encode, arrow_encode_embed, arrow_prompt_encode, arrow_encode_embed,
        #     line_circle, text_dim1, text_dim2
        # )
        self.add(self.unet)
        self.play(Create(self.prompt), GrowArrow(arrow_prompt_encode), GrowFromCenter(self.model_text_encoder))
        self.play(
            Rotate(self.gears_text_encoder[0], axis=IN,
                   about_point=self.gears_text_encoder[0].get_center()),
            GrowArrow(arrow_encode_embed),
            Create(embedding_prompt)
        )
        self.play(FadeIn(noise, shift=DOWN), Write(text_dim1))
        self.play(
            GrowArrow(arrow_embedding),
            LaggedStartMap(Create, line_embedding_unet, lag_ratio=0.01)
        )
        self.play(
            FadeOut(noise, scale=0.1, target_position=self.unet.get_left()),
            FadeOut(text_dim1),
            LaggedStart(
                *[p.animate(rate_func=there_and_back).set_color(TEAL)
                  for prism in self.unet[0] for p in prism],
                lag_ratio=0.1, run_time=3
            ),
            ShowPassingFlash(line_embedding, time_width=0.2, run_time=3),
            LaggedStartMap(
                ShowPassingFlash, line_embedding_unet.copy().set_stroke(RED, 5.0),
                time_width=0.3,
                lag_ratio=0.1,
                run_time=3
            )
        )
        self.play(
            FadeIn(noise_out, scale=0.1, target_position=self.unet.get_right()),
            Write(text_steps[0]),
            Write(text_dim2)
        )
        self.wait()
        self.play(
            FadeOut(text_dim2),
            MoveAlongPath(noise_out, line_circle, run_time=2),
        )
        self.play(
            FadeOut(noise_out, scale=0.1, target_position=self.unet.get_left()),
            LaggedStart(
                *[p.animate(rate_func=there_and_back).set_color(TEAL)
                  for prism in self.unet[0] for p in prism],
                lag_ratio=0.1, run_time=2
            ),
            ShowPassingFlash(line_embedding, time_width=0.2, run_time=2),
            LaggedStartMap(
                ShowPassingFlash, line_embedding_unet.copy().set_stroke(RED, 5.0),
                time_width=0.3,
                lag_ratio=0.1,
                run_time=2
            )
        )
        noise_out.move_to(3.8 * RIGHT + 0.7 * UP)
        self.play(
            FadeIn(noise_out, scale=0.1, target_position=self.unet.get_right()),
            FadeTransform(text_steps[0], text_steps[1])
        )
        self.wait()
        for i in range(1, 7):
            self.play(
                FadeTransform(text_steps[i], text_steps[i + 1]),
                ShowPassingFlash(line_circle.copy().set_stroke(RED, 3.0), time_width=0.5, run_time=0.3),
                LaggedStart(
                    *[p.animate(rate_func=there_and_back).set_color(TEAL)
                      for prism in self.unet[0] for p in prism],
                    lag_ratio=0.1, run_time=0.3
                )
            )
        for i in range(7, len(text_steps) - 1):
            self.play(
                FadeTransform(text_steps[i], text_steps[i + 1], run_time=0.09),
                LaggedStart(
                    *[p.animate(rate_func=there_and_back).set_color(TEAL)
                      for prism in self.unet[0] for p in prism],
                    lag_ratio=0.1, run_time=0.09
                )
            )
        self.play(GrowArrow(arrow_out_decode), GrowFromCenter(self.model_vae_decoder))
        self.play(
            GrowArrow(arrow_decode_image),
            Rotate(self.gears_vae_decoder[0], axis=IN,
                   about_point=self.gears_vae_decoder[0].get_center()),
            FadeIn(image_prompt, shift=DOWN))

        self.wait()

    def construct(self):
        self.camera.background_color = "#1C1C1C"
        self.ddpm1()
        self.ddpm2()
        self.ddpm3()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.latent1()
        self.latent2()


if __name__ == "__main__":
    Models().render()
