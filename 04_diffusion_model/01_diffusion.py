import random

from PIL import Image

from utils import *


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
                buff=0.2, color=GREY, corner_radius=0.3, stroke_width=2.0
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
                buff=0.2, color=GREY, corner_radius=0.3, stroke_width=2.0
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
            self.gear.copy().scale(0.4).shift(0.52 * RIGHT).set_color(GREEN_C),
            self.gear.copy().scale(0.4).shift(0.52 * LEFT).set_color(GOLD_C)
        )
        text_vqvae = Text(
            "VQVAE", font="Menlo", font_size=20, color=GREY
        ).shift(0.8 * DOWN)
        self.model_vqvae = VGroup(
            trapezoid_right, trapezoid_left, self.gears_vqvae, text_vqvae,
            # SurroundingRectangle(
            #     VGroup(trapezoid_right, trapezoid_left, text_vqvae),
            #     buff=0.15, color=GREY, corner_radius=0.3, stroke_width=2.0
            # )
        )

        # ==============================================================
        # title
        self.title = Text("How does diffusion model work")
        self.logo = MathTex(
            r"\mathbb{JAYANDJEAN}", fill_color="#ece6e2"
        ).next_to(self.title, DOWN, buff=0.5).scale(1.2)
        self.title_clip = Text("CLIP", font="Menlo").to_edge(UL, buff=0.5).scale(0.7)
        self.title_ddpm = Text("DDPM", font="Menlo").to_edge(UL, buff=0.5).scale(0.7)

    def ddpm0(self):
        # 2. show diffusion products
        # 清理干净
        # mid_feed = ImageMobject("assets/Midjourney-Feed.png").set(width=12).to_edge(UP)
        # mid_feed.generate_target()
        # mid_feed.target.to_edge(DOWN)
        # mid = ImageMobject("assets/product_mid.jpg").set(height=2)
        # sd3 = ImageMobject("assets/product_sd3.png").set(height=2)
        # flux = ImageMobject("assets/product_flux.png").set(height=2)
        # models = Group(mid, sd3, flux).arrange(RIGHT, buff=0.2).align_to(LEFT)
        # todo: 需要补充内容
        # self.play(LaggedStartMap(FadeIn, models, lag_ratio=0.5))
        # self.play(FadeOut(models))
        # self.wait()
        # self.add(mid_feed)
        # self.play(MoveToTarget(mid_feed, run_time=13, rate_func=linear))

        # FLux
        text1 = Text("cybotix style, a close-up of a robotic bee hovering in the air")
        text2 = Text(
            "Create an image of a surreal and fantastical creature inspired by Salvador Dalí's style. The creature should have a blend of dreamlike and bizarre elements, combining various animal forms with unexpected, imaginative features. Incorporate melting or distorted shapes, unusual textures, and an overall ethereal and otherworldly atmosphere. Use vivid, contrasting colors and play with perspective to evoke a sense of the uncanny and the extraordinary.")

    def ddpm1(self):
        # 3. show generating images
        image_prompt = ImageMobject("assets/prompt.png").set(width=4.2)

        embedding_prompt = WeightMatrix(length=15).set(width=0.5)
        matrix_image = VGroup(
            WeightMatrix(shape=(14, 8)).set(width=4).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP),
            WeightMatrix(shape=(14, 8)).set(width=4).set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP),
            WeightMatrix(shape=(14, 8)).set(width=4),
        )

        text_prompt = Paragraph("a cyberpunk with ",
                                "natural greys and ",
                                "whites and browns.",
                                line_spacing=1.0, font="Menlo").scale(0.4)
        surrounding_prompt = SurroundingRectangle(
            text_prompt, buff=0.2, color=WHITE, corner_radius=0.3, stroke_width=0.5)
        prompt = VGroup(surrounding_prompt, text_prompt)
        Group(prompt, embedding_prompt, self.model_diffusion, matrix_image).arrange(RIGHT, buff=1.0)
        arrow_prompt_embedding = Arrow(prompt.get_right(), embedding_prompt.get_left())
        arrow_embedding_model = Arrow(embedding_prompt.get_right(), self.model_diffusion.get_left())
        arrow_model_matrix = Arrow(self.model_diffusion.get_right(), matrix_image.get_left())
        image_prompt.move_to(matrix_image.get_center())

        self.play(FadeIn(self.model_diffusion))
        self.play(Create(prompt))
        self.play(
            GrowArrow(arrow_prompt_embedding),
            Indicate(embedding_prompt)
        )
        self.play(
            GrowArrow(arrow_embedding_model),
            LaggedStart(
                AnimationGroup(
                    Rotate(self.gears_diffusion[i], axis=IN if i == 0 else OUT,
                           about_point=self.gears_diffusion[i].get_center())
                    for i in range(3)
                ), run_time=4, lag_ratio=0.0)
        )
        self.play(GrowArrow(arrow_model_matrix), Create(matrix_image))
        self.play(FadeIn(image_prompt), FadeOut(matrix_image))
        self.play(FadeOut(image_prompt, arrow_prompt_embedding, arrow_embedding_model, arrow_model_matrix, prompt))
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
        for i in range(4):
            self.play(
                LaggedStartMap(RandomizeMatrixEntries, VGroup(matrix1[0], matrix2[0], matrix3[0]), lag_ratio=0.1),
                LaggedStart(
                    AnimationGroup(
                        Rotate(self.gears_diffusion[i],
                               axis=IN if i == 0 else OUT,
                               about_point=self.gears_diffusion[i].get_center())
                        for i in range(3)
                    ), run_time=2, lag_ratio=0.0),
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
        self.play(FadeIn(self.model_diffusion, shift=DOWN))
        self.play(FadeIn(image_noise, shift=DOWN), Write(prompt_cat))
        self.play(GrowArrow(arrow_noise_model),
                  GrowArrow(arrow_prompt_model),
                  LaggedStart(
                      AnimationGroup(
                          Rotate(self.gears_diffusion[i], axis=IN if i == 0 else OUT,
                                 about_point=self.gears_diffusion[i].get_center())
                          for i in range(3)
                      ), run_time=2, lag_ratio=0.0)
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
        self.play(FadeOut(line_800, dot_alpha_800, dot_one_minus_alpha_800,
                          line_50, dot_alpha_50, dot_one_minus_alpha_50,
                          one_minus_alpha_curve, one_minus_alpha_label,
                          alpha_curve, alpha_label, axes, formula_xt))
        self.play(FadeOut(image_cat_50, image_cat_800))
        self.wait()

    def ddpm3(self):
        # 5.4 train model
        # 清理干净
        image_encode_set = Group(
            *[Group(*([ele for j in [f"assets/cat_{i}{f}" for f in ('.jpg', '_0040.png', '_0060.png', '_0080.png')]
                       for ele in [ImageMobject(j).set(width=2), Text("···").scale(0.5)]] +
                      [ImageMobject(f"assets/cat_{i}_0999.png").set(width=2)]
                      )
                    ).arrange(RIGHT, buff=0.3)
              for i in range(3)]
        ).arrange(DOWN, buff=0.3).move_to(DOWN)

        image_encode_set.generate_target()
        image_encode_set.target.scale(0.6).move_to(1.6 * UP)
        brace_image_set = Brace(image_encode_set.target, direction=DOWN)
        self.model_diffusion.next_to(brace_image_set, DOWN)
        formula_encode = MathTex(
            r"\operatorname{loss}=|\boldsymbol{\epsilon}-",
            r"\boldsymbol{\epsilon}_\theta",
            r"(\mathbf{x}_t, t)\|^2"
        ).next_to(brace_image_set, DOWN)
        formula_decode = MathTex(
            r"\mathbf{x}_{t-1}",
            r"=",
            r"\frac{1}{\sqrt{\alpha_t}}\left(",
            r"\mathbf{x}_t-",
            r"\frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} ",
            r"\boldsymbol{\epsilon}_\theta",
            r"\left(\mathbf{x}_t, t\right)\right)+\sigma_t \mathbf{z}"
        ).scale(0.7).move_to(self.model_diffusion.get_top() + 1 * UP + RIGHT)

        box_encode = SurroundingRectangle(
            formula_encode[1], corner_radius=0.01
        ).set_stroke(YELLOW_E, 2.0)
        box_decode_model = SurroundingRectangle(
            formula_decode[5], corner_radius=0.01
        ).set_stroke(YELLOW_E, 2.0)
        image_unet = ImageMobject("assets/unet.png").set(width=4).next_to(formula_encode, DOWN, buff=0.5)
        image_path_list = [ImageMobject(f"assets/cat_out_0000.jpg").set(width=2)] + \
                          [ImageMobject(f"assets/cat_out_{i:04}.png").set(width=2)
                           for i in list(range(5, 255, 5))]
        image_output_cats = Group(*image_path_list[::-1])
        image_input_noise = (ImageMobject("assets/cat_out_0999.png").set(width=2)
                             .next_to(self.model_diffusion, LEFT, buff=1.5))
        image_output_dog = (ImageMobject("assets/dog_out.jpg").set(width=2)
                            .next_to(self.model_diffusion, RIGHT, buff=1.5))

        arrow_input_model = Arrow(image_input_noise.get_right(), self.model_diffusion.get_left())
        arrow_model_output = Arrow(self.model_diffusion.get_right(), image_output_dog.get_left())
        text_steps = VGroup(
            *[
                Text(
                    f"Step {i + 1}", font="Menlo", font_size=35, color=GREY
                ).next_to(image_output_dog, UP)
                for i in range(len(image_output_cats))
            ]
        )
        line_circle = CubicBezier(
            image_output_dog.get_right(),
            image_output_dog.get_right() + 8 * RIGHT + 3 * UP,
            self.model_diffusion.get_left() + 8 * LEFT + 6 * UP,
            self.model_diffusion.get_left()
        )
        line_circle.z_index = -1

        # self.add(self.model_diffusion, formula_decode, line_circle, image_output_dog,
        #          image_input_noise, arrow_input_model, arrow_model_output)

        self.play(LaggedStartMap(FadeIn, image_encode_set, lag_ratio=0.5))
        self.play(MoveToTarget(image_encode_set), GrowFromCenter(brace_image_set))
        self.play(Write(formula_encode), Create(box_encode))
        self.play(FadeIn(image_unet))
        self.play(FadeOut(image_unet, box_encode))
        self.play(FadeTransform(formula_encode, self.model_diffusion))
        self.play(FadeOut(image_encode_set, brace_image_set))

        for i in range(len(image_output_cats) - 1):
            image_output_cats[i + 1].next_to(self.model_diffusion, RIGHT, buff=1.5)
            if i == 0:
                image_output_cats[i].next_to(self.model_diffusion, LEFT, buff=1.5)
                self.play(FadeIn(image_output_cats[i], shift=DOWN), GrowArrow(arrow_input_model))
                self.play(Write(formula_decode))
                self.play(Create(box_decode_model))
                self.play(GrowArrow(arrow_model_output), FadeIn(image_output_cats[i + 1]))
                self.play(Write(text_steps[i]))
                self.play(Create(line_circle))
            elif i <= 2:
                if i == 1:
                    self.play(FadeOut(image_output_cats[0], arrow_input_model))
                im = image_output_cats[i].copy()
                self.play(MoveAlongPath(im, line_circle, run_time=1.5))
                self.play(
                    FadeOut(im, target_position=image_output_dog),
                    FadeIn(image_output_cats[i + 1]),
                    FadeTransform(text_steps[i - 1], text_steps[i]),
                    run_time=0.5
                )
            elif i <= 7:
                self.play(ShowPassingFlash(line_circle.copy().set_color(RED), run_time=0.5, time_width=1.0))
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
        self.play(
            FadeOut(formula_decode, line_circle, text_steps[49], box_decode_model)
        )
        self.play(Group(self.model_diffusion, arrow_model_output,
                        image_output_cats[1:51]).animate.shift(LEFT + 2 * UP))

        image_output_dog.next_to(self.model_diffusion, RIGHT, buff=1.5)
        text_question = Text("?").scale(3).next_to(image_output_dog, RIGHT)
        self.play(
            FadeIn(image_output_dog, shift=DOWN),
            image_output_cats[1:51].animate.next_to(image_output_dog, DOWN),
            Create(text_question)
        )
        self.play(FadeOut(image_output_dog, self.model_diffusion,
                          arrow_model_output, text_question, image_output_cats[1:51]))
        self.wait()

    def clip1(self):
        # 7. show part
        # 还有model_clip
        self.play(FadeTransform(self.title_ddpm, self.title_clip))
        text_encoder = VGroup(self.gear.copy().scale(0.4).set_color(BLUE_C),
                              Text("Text Encoder", font="Menlo", font_size=30)).arrange(RIGHT, buff=0.5)
        image_encoder = VGroup(self.gear.copy().scale(0.4).set_color(BLUE_E),
                               Text("Image Encoder", font="Menlo", font_size=30)).arrange(RIGHT, buff=0.5)
        encoders = VGroup(text_encoder, image_encoder).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        brace_clip = Brace(encoders, direction=LEFT, buff=0.5)
        VGroup(self.model_clip, brace_clip, encoders).arrange(RIGHT, buff=0.7)

        self.play(FadeIn(self.model_clip))
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
        last_pos = 5 * RIGHT + 1.5 * UP

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

        image_cat = ImageMobject("assets/cat_out_0000.jpg").set(height=2).move_to(input_pos)
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

        image_dog = ImageMobject("assets/dog_out.jpg").set(height=2).move_to(input_pos)
        embedding_image_dog = WeightMatrix(length=14).set(width=0.5).move_to(output_pos)
        embedding_image_dog.generate_target()
        embedding_image_dog.target.set(width=0.4).move_to(last_pos + 1.8 * LEFT)
        image_dog.generate_target()
        image_dog.target.set(width=0.45).next_to(embedding_image_dog.target, UP)

        self.play(Create(text_cat))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                           about_point=self.gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(text_cat, embedding_text_cat))
        )
        self.play(GrowFromCenter(brace_text), Create(dim_text))
        self.play(FadeOut(brace_text, dim_text))
        self.play(MoveToTarget(embedding_text_cat), MoveToTarget(text_cat))

        self.play(FadeIn(image_cat))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                           about_point=self.gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(image_cat, embedding_image_cat, path_arc=-30 * DEGREES))
        )
        self.play(GrowFromCenter(brace_text), Create(dim_text))
        self.play(FadeOut(brace_text, dim_text))
        self.play(MoveToTarget(embedding_image_cat), MoveToTarget(image_cat))

        self.play(Create(text_dog))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                           about_point=self.gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(text_dog, embedding_text_dog)),
        )
        self.play(MoveToTarget(embedding_text_dog), MoveToTarget(text_dog))

        self.play(FadeIn(image_dog))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                           about_point=self.gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(image_dog, embedding_image_dog, path_arc=-30 * DEGREES))
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
            embedding_text_cat, text_cat, self.logo, self.title_clip
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
        text_words = VGroup(*[Text(word, font="Menlo").scale(0.4) for word in words])
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
        text_tokenizer = Text("Tokenizer", font_size=24).set_color(YELLOW_E).next_to(brace_numbers, LEFT)

        embedding_words = VGroup(*[WeightMatrix(length=10).set(width=0.5).next_to(rect, DOWN, buff=2.0)
                                   for rect in rect_words])
        arrow_embeds = VGroup(*[Arrow(text_numbers[i].get_bottom(), embedding_words[i].get_top())
                                for i in range(len(rect_words))])

        emb_syms = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}").next_to(rect, DOWN, buff=0.75).set_color(GREY_A)
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
        emb_sym_primes = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}^{{'}}").move_to(sym.get_center() + 4 * DOWN)
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
        dim_text = Text("768-dimensional", font_size=24).set_color(YELLOW_E).next_to(brace_text, RIGHT)
        self.model_clip.move_to(5 * LEFT)

        self.play(FadeIn(self.model_clip))
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

        image_emb_syms = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}").next_to(im, DOWN, buff=0.75).set_color(GREY_A)
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
        emb_sym_primes = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}^{{'}}").move_to(sym.get_center() + 4 * DOWN)
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
            ImageMobject("assets/cat_out_0000.jpg").set(width=2).set_opacity(1.0),
            ImageMobject("assets/cat_out_0000.jpg").set(width=2).set_opacity(0.4).shift(0.1 * UP + 0.1 * RIGHT),
            ImageMobject("assets/cat_out_0000.jpg").set(width=2).set_opacity(0.3).shift(0.2 * UP + 0.2 * RIGHT),
            ImageMobject("assets/cat_out_0000.jpg").set(width=2).set_opacity(0.2).shift(0.3 * UP + 0.3 * RIGHT),
            ImageMobject("assets/cat_out_0000.jpg").set(width=2).set_opacity(0.1).shift(0.4 * UP + 0.4 * RIGHT),
            ImageMobject("assets/cat_out_0000.jpg").set(width=2).set_opacity(0.05).shift(0.5 * UP + 0.5 * RIGHT),
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

    def latent1(self):
        pass

    def construct(self):
        self.camera.background_color = "#1C1C1C"
        # self.play(Write(self.title))
        # self.play(Write(self.logo))
        # self.play(
        #     FadeOut(self.title),
        #     self.logo.animate.scale(0.4).move_to(RIGHT * 5.5 + UP * 3.5)
        # )
        # self.wait()
        self.ddpm2()
        # self.ddpm1()
        # self.ddpm2()
        # self.ddpm3()
        # self.clip1()
        # self.clip2()
        # self.clip3()
        # self.clip4()
        # self.clip5()
        # self.latent1()

        # self.model_diffusion.move_to(ORIGIN)
        # self.model_clip.move_to(4 * LEFT + 2 * DOWN)
        # self.model_vqvae.move_to(4 * LEFT + 2 * UP)
        # self.add(self.model_diffusion, self.model_clip, self.model_vqvae)


if __name__ == "__main__":
    Diffusion().render()
