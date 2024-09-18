from utils import *


# 满意
class DDPM1(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        # 1. title
        title = Text("How does diffusion model work")
        logo = MathTex(r"\mathbb{JAYANDJEAN}", fill_color="#ece6e2").next_to(title, DOWN, buff=0.5).scale(1.2)
        self.play(Write(title))
        self.play(Write(logo))
        self.play(
            FadeOut(title),
            logo.animate.scale(0.4).move_to(RIGHT * 5.5 + UP * 3.5)
        )
        self.wait()

        # 2. show diffusion products
        mid = ImageMobject("assets/mid.jpg").set(height=2)
        sd3 = ImageMobject("assets/sd3.png").set(height=2)
        flux = ImageMobject("assets/flux.png").set(height=2)
        models = Group(mid, sd3, flux).arrange(RIGHT, buff=0.2).align_to(LEFT)
        # todo: 需要补充内容
        self.play(LaggedStartMap(FadeIn, models, lag_ratio=0.5))
        self.play(FadeOut(models))
        self.wait()

        # 3. show generating images
        gear = SVGMobject("assets/wheel.svg")
        image_prompt = ImageMobject("assets/prompt.png").set(width=4.2)
        gears = VGroup(gear.copy().scale(0.5).shift(0.78 * UP).set_color(YELLOW),
                       gear.copy().scale(0.5).shift(0.57 * LEFT).set_color(ORANGE),
                       gear.copy().scale(0.5).shift(0.57 * RIGHT))
        text_model = Text("Diffusion Model", font_size=24, color=GREY).next_to(gears, DOWN, SMALL_BUFF)
        surrounding_model = SurroundingRectangle(VGroup(gears, text_model),
                                                 buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        model_diffusion = VGroup(gears, text_model, surrounding_model)

        embedding_prompt = WeightMatrix(length=15).set(width=0.5)
        matrix_image = VGroup(
            WeightMatrix(shape=(14, 8)).set(width=4).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP),
            WeightMatrix(shape=(14, 8)).set(width=4).set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP),
            WeightMatrix(shape=(14, 8)).set(width=4),
        )

        text_prompt = Paragraph("a cyberpunk with ",
                                "natural greys and ",
                                "whites and browns.",
                                line_spacing=1.0, font="menlo").scale(0.4)
        surrounding_prompt = SurroundingRectangle(text_prompt,
                                                  buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        prompt = VGroup(surrounding_prompt, text_prompt)
        Group(prompt, embedding_prompt, model_diffusion, matrix_image).arrange(RIGHT, buff=1.0)
        arrow_prompt_embedding = Arrow(prompt.get_right(), embedding_prompt.get_left())
        arrow_embedding_model = Arrow(embedding_prompt.get_right(), model_diffusion.get_left())
        arrow_model_matrix = Arrow(model_diffusion.get_right(), matrix_image.get_left())
        image_prompt.move_to(matrix_image.get_center())

        self.play(FadeIn(model_diffusion))
        self.play(Create(prompt))
        self.play(
            GrowArrow(arrow_prompt_embedding),
            Indicate(embedding_prompt)
        )
        self.play(
            GrowArrow(arrow_embedding_model),
            LaggedStart(
                AnimationGroup(
                    Rotate(gears[i], axis=IN if i == 0 else OUT, about_point=gears[i].get_center())
                    for i in range(3)
                ), run_time=4, lag_ratio=0.0)
        )
        self.play(GrowArrow(arrow_model_matrix), Create(matrix_image))
        self.play(FadeIn(image_prompt), FadeOut(matrix_image))
        self.play(FadeOut(image_prompt, arrow_prompt_embedding, arrow_embedding_model, arrow_model_matrix, prompt))
        self.wait()

        # 3.1. why we need embedding
        model_diffusion.generate_target()
        box = Rectangle(width=9.5, height=4.5).set_fill(GREY_E, 1).set_stroke(WHITE, 1)
        VGroup(model_diffusion.target, box).arrange(RIGHT, buff=1)
        line1 = Line(start=model_diffusion.target.get_corner(direction=UR),
                     end=box.get_corner(direction=UL)).set_stroke(WHITE, 1)
        line2 = Line(start=model_diffusion.target.get_corner(direction=DR),
                     end=box.get_corner(direction=DL)).set_stroke(WHITE, 1)

        self.play(Wiggle(embedding_prompt))
        self.play(FadeOut(embedding_prompt), MoveToTarget(model_diffusion))
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
        for i in range(4):
            self.play(
                LaggedStartMap(RandomizeMatrixEntries, VGroup(matrix1[0], matrix2[0], matrix3[0]), lag_ratio=0.1),
                LaggedStart(
                    AnimationGroup(
                        Rotate(gears[i],
                               axis=IN if i == 0 else OUT,
                               about_point=gears[i].get_center())
                        for i in range(3)
                    ), run_time=2, lag_ratio=0.0),
            )
        self.play(FadeOut(all_matrix))
        self.play(FadeOut(box, line1, line2, model_diffusion))
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


class DDPM2(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        gear = SVGMobject("assets/wheel.svg")
        image_prompt = ImageMobject("assets/prompt.png").set(width=4.2)
        gears = VGroup(gear.copy().scale(0.5).shift(0.78 * UP).set_color(YELLOW),
                       gear.copy().scale(0.5).shift(0.57 * LEFT).set_color(ORANGE),
                       gear.copy().scale(0.5).shift(0.57 * RIGHT))
        text_model = Text("Diffusion Model", font_size=24, color=GREY).next_to(gears, DOWN, SMALL_BUFF)
        surrounding_model = SurroundingRectangle(VGroup(gears, text_model),
                                                 buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        model_diffusion = VGroup(gears, text_model, surrounding_model)

        # 4. 目录
        title_papers = VGroup(
            Text("2020.06 \nDenoising Diffusion Probabilistic Models",
                 font="menlo", t2c={'D': YELLOW, 'P': YELLOW, 'M': YELLOW}),
            Text("2021.03 \nContrastive Language-Image Pre-Training",
                 font="menlo", t2c={'C': YELLOW, 'L': YELLOW, 'I': YELLOW, 'P': YELLOW}),
            Text("2021.12 \nLatent Diffusion Models", font="menlo"),
            Text("2024.03 \nStable Diffusion 3", font="menlo"),
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
        model_diffusion.move_to(ORIGIN)
        text_ddpm = Text("DDPM", font="menlo").to_edge(UL, buff=0.5).scale(0.7)
        text_prompt_cat = Text("a photo of a cat", font="menlo").scale(0.4)
        surrounding_prompt_cat = SurroundingRectangle(text_prompt_cat,
                                                      buff=0.1, color=WHITE, corner_radius=0.1).set_stroke(width=0.5)
        prompt_cat = VGroup(text_prompt_cat, surrounding_prompt_cat).move_to(3 * UP)
        arrow_prompt_model = Arrow(prompt_cat.get_bottom(), model_diffusion.get_top())
        image_noise = ImageMobject("assets/cat_0_0999.png").set(width=4).move_to(4.5 * LEFT)
        image_cat_35 = ImageMobject("assets/cat_0_0035.png").set(width=4).move_to(4.5 * LEFT)
        image_cat = ImageMobject("assets/cat_0.jpg").set(width=4).move_to(4.5 * RIGHT)
        arrow_noise_model = Arrow(image_noise.get_right(), model_diffusion.get_left())
        arrow_model_cat = Arrow(model_diffusion.get_right(), image_cat.get_left())
        hard = Text("Hard!").scale(0.9).move_to(3 * RIGHT + 2.5 * UP)
        easy = Text("Easy!").scale(0.9).move_to(3 * RIGHT + 2.5 * UP)
        self.play(
            FadeOut(image_papers),
            FadeTransform(VGroup(title_papers, arrow_history, dot_papers), text_ddpm)
        )
        self.play(FadeIn(model_diffusion, shift=DOWN))
        self.play(FadeIn(image_noise, shift=DOWN), Write(prompt_cat))
        self.play(GrowArrow(arrow_noise_model),
                  GrowArrow(arrow_prompt_model),
                  LaggedStart(
                      AnimationGroup(
                          Rotate(gears[i], axis=IN if i == 0 else OUT, about_point=gears[i].get_center())
                          for i in range(3)
                      ), run_time=2, lag_ratio=0.0)
                  )
        self.play(GrowArrow(arrow_model_cat), FadeIn(image_cat, shift=DOWN))
        self.play(Indicate(hard))
        self.play(FadeOut(image_noise, shift=DOWN))
        self.play(FadeIn(image_cat_35, shift=DOWN), FadeOut(hard))
        self.play(Indicate(easy))
        self.play(FadeOut(easy, arrow_model_cat, model_diffusion, arrow_noise_model,
                          arrow_prompt_model, prompt_cat))
        self.wait()

        # 5.1 Decode
        path_cats = (["assets/cat_0.jpg"] +
                     [f"assets/cat_0_00{i}.png" for i in range(35, 96, 5)] +
                     ["assets/cat_0_0999.png"])
        image_cats_decode_15 = Group(
            *[Group(
                *[ImageMobject(path_cats[j]) for j in range(i * 5, (i + 1) * 5)]
            ).set(height=1.8).arrange(LEFT if i != 1 else RIGHT, buff=0.3) for i in range(3)]
        ).arrange(DOWN, buff=0.3).shift(0.5 * DOWN)

        image_cats_decode_5 = Group(
            *([ele for i in [f"assets/{f}" for f in ['cat_0_0999.png', 'cat_0_0095.png',
                                                     'cat_0_0065.png', 'cat_0_0035.png']]
               for ele in [ImageMobject(i).set(height=1.4), Text("···").scale(0.7)]] +
              [ImageMobject("assets/cat_0.jpg").set(height=1.4)]
              )
        ).arrange(RIGHT, buff=0.3)

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
        images_and_lines.target.scale(0.7).to_edge(RIGHT)
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
            *([ele for i in [f"assets/{f}" for f in ['cat_0.jpg', 'cat_0_0065.png', 'cat_0_0999.png', 'cat_0_0065.png']]
               for ele in [ImageMobject(i).set(height=1.4), Text("···").scale(0.7)]] +
              [ImageMobject("assets/cat_0.jpg").set(height=1.4)]
              )
        ).arrange(RIGHT, buff=0.3)

        image_cats_encode_5 = Group(
            *([ele for i in [f"assets/{f}" for f in ['cat_0.jpg', 'cat_0_0040.png', 'cat_0_0060.png', 'cat_0_0080.png']]
               for ele in (ImageMobject(i).set(height=1.4), Text("···").scale(0.7))] +
              [ImageMobject("assets/cat_0_0999.png").set(height=1.4)]
              )
        ).arrange(RIGHT, buff=0.3)

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
                                         line_config={"color": YELLOW, "dashed_ratio": 0.85})
        line_800 = axes.get_vertical_line(axes.c2p(800, 1),
                                          line_config={"color": YELLOW, "dashed_ratio": 0.85})

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
        image_cat_50 = ImageMobject("assets/cat_0_0050.png").set(height=2).next_to(line_50, RIGHT)
        image_cat_800 = ImageMobject("assets/cat_0_0999.png").set(height=2).next_to(line_800, LEFT)

        self.play(formula_xt.animate.to_edge(UP).scale(0.8))

        self.play(Create(axes))
        self.play(Create(alpha_curve), Write(alpha_label))
        self.play(Create(one_minus_alpha_curve), Write(one_minus_alpha_label))
        self.play(Create(line_50), Create(dot_alpha_50), Create(dot_one_minus_alpha_50))
        self.play(Create(line_800), Create(dot_alpha_800), Create(dot_one_minus_alpha_800))
        self.play(FadeIn(image_cat_50), FadeIn(image_cat_800))
        self.wait()

        # 5.4 train model
        image_encode_set = Group(
            *[Group(*([ele for j in [f"assets/cat_{i}{f}" for f in ('.jpg', '_0040.png', '_0060.png', '_0080.png')]
                       for ele in [ImageMobject(j).set(width=2), Text("···").scale(0.5)]] +
                      [ImageMobject(f"assets/cat_{i}_0999.png").set(width=2)]
                      )
                    ).arrange(RIGHT, buff=0.3)
              for i in range(3)]
        ).arrange(DOWN, buff=0.3).move_to(DOWN)

        image_encode_set.generate_target()
        image_encode_set.target.scale(0.6).move_to(UP)
        brace_image_set = Brace(image_encode_set.target, direction=DOWN)
        formula_encode = MathTex(r"\nabla_\theta\|\boldsymbol{\epsilon}-",
                                 r"\boldsymbol{\epsilon}_\theta",
                                 r"(\mathbf{x}_t, t)\|^2").next_to(brace_image_set, DOWN)
        frame_box_model = SurroundingRectangle(formula_encode[1], corner_radius=0.01).set_stroke(width=2.0)
        image_unet = ImageMobject("assets/unet.png").set(width=4).next_to(formula_encode, DOWN, buff=.1)
        model_diffusion.next_to(brace_image_set, DOWN)

        self.play(FadeOut(image_cat_50, image_cat_800,
                          line_800, dot_alpha_800, dot_one_minus_alpha_800,
                          line_50, dot_alpha_50, dot_one_minus_alpha_50,
                          one_minus_alpha_curve, one_minus_alpha_label,
                          alpha_curve, alpha_label, axes, formula_xt))
        self.play(LaggedStartMap(FadeIn, image_encode_set, lag_ratio=1.0))
        self.play(MoveToTarget(image_encode_set), GrowFromCenter(brace_image_set))
        self.play(Write(formula_encode), Create(frame_box_model))
        self.play(FadeIn(image_unet))
        self.play(FadeOut(image_unet, frame_box_model))
        self.play(Transform(formula_encode, model_diffusion))

        image_input_noise = ImageMobject("assets/cat_out_0999.png").set(width=2).next_to(formula_encode, LEFT, buff=1)
        image_output_cat = ImageMobject("assets/cat_out.jpg").set(width=2).next_to(formula_encode, RIGHT, buff=1)
        image_output_dog = ImageMobject("assets/dog_out.jpg").set(width=2).next_to(formula_encode, RIGHT, buff=1)
        text_question = Text("?").scale(3).next_to(image_output_dog, RIGHT)
        arrow_input_model = Arrow(image_input_noise.get_right(), formula_encode.get_left())
        arrow_model_output = Arrow(formula_encode.get_right(), image_output_cat.get_left())

        self.play(FadeIn(image_input_noise), GrowArrow(arrow_input_model))
        self.play(GrowArrow(arrow_model_output), FadeIn(image_output_cat))
        self.play(Transform(image_output_cat, image_output_dog), Create(text_question))
        self.play(FadeOut(image_output_cat, text_question, arrow_input_model, arrow_model_output, image_input_noise,
                          formula_encode, image_encode_set, brace_image_set, text_ddpm))
        self.wait()


if __name__ == "__main__":
    scene = DDPM2()
    scene.render()
