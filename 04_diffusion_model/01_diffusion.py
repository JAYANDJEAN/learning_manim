from utils import *


class Models(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        # 1. title
        title = Text("How does diffusion model work")
        logo = MathTex(r"\mathbb{JAYANDJEAN}", fill_color="#ece6e2").next_to(title, DOWN, buff=0.5).scale(1.2)
        self.play(Write(title))
        self.play(Write(logo))
        self.play(FadeOut(title), logo.animate.scale(0.4).move_to(RIGHT * 5.5 + UP * 3.5))
        self.wait()

        # 2. show diffusion products
        mid = ImageMobject("assets/mid.jpg").set(height=2)
        sd3 = ImageMobject("assets/sd3.png").set(height=2)
        flux = ImageMobject("assets/flux.png").set(height=2)
        models = Group(mid, sd3, flux).arrange(RIGHT, buff=0.2).align_to(LEFT)
        # todo: 需要补充内容
        self.play(LaggedStartMap(FadeIn, models, lag_ratio=1.0, run_time=3))
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
            WeightMatrix(shape=(12, 7)).set(width=4).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP),
            WeightMatrix(shape=(12, 7)).set(width=4).set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP),
            WeightMatrix(shape=(12, 7)).set(width=4),
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

        self.play(FadeOut(models))
        self.play(FadeIn(model_diffusion))
        self.play(Create(prompt))
        self.play(GrowArrow(arrow_prompt_embedding), Indicate(embedding_prompt))
        self.play(GrowArrow(arrow_embedding_model),
                  LaggedStart(
                      AnimationGroup(
                          Rotate(gears[i], axis=IN if i == 0 else OUT, about_point=gears[i].get_center())
                          for i in range(3)
                      ), run_time=4, lag_ratio=0.0))
        self.play(GrowArrow(arrow_model_matrix), Create(matrix_image))
        self.wait()
        self.play(FadeIn(image_prompt), FadeOut(matrix_image))
        self.wait()

        # 3.1. why we need embedding
        model_diffusion.generate_target()
        box = Rectangle(width=9.5, height=4.5).set_fill(GREY_E, 1).set_stroke(WHITE, 1)
        VGroup(model_diffusion.target, box).arrange(RIGHT, buff=1)
        line1 = Line(start=model_diffusion.target.get_corner(direction=UR),
                     end=box.get_corner(direction=UL)).set_stroke(WHITE, 1)
        line2 = Line(start=model_diffusion.target.get_corner(direction=DR),
                     end=box.get_corner(direction=DL)).set_stroke(WHITE, 1)
        # shape_list = [[(7, 7), (7, 6), (7, 6)],
        #               [(8, 6), (6, 6), (8, 6)],
        #               [(8, 5), (5, 6), (8, 6)],
        #               [(7, 7), (7, 6), (7, 6)],
        #               [(8, 6), (6, 6), (8, 6)]]
        # matrix_mul = []
        # for i, shapes in enumerate(shape_list):
        #     matrix1, matrix2, matrix3 = [
        #         VGroup(WeightMatrix(shape=shape).set(width=0.4 * shape[1]),
        #                WeightMatrix(shape=shape).set(width=0.4 * shape[1])
        #                .set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP),
        #                WeightMatrix(shape=shape).set(width=0.4 * shape[1])
        #                .set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP)
        #                ) for shape in shapes]
        #     eq = Tex('=')
        #     all_matrix = (VGroup(matrix1, matrix2, eq, matrix3)
        #                   .arrange(RIGHT, buff=0.2)
        #                   .move_to(box.get_center()))
        #     matrix_mul.append(Animation()
        #                       # Succession(
        #                       #     Create(VGroup(matrix1, matrix2, eq)),
        #                       #     TransformFromCopy(VGroup(matrix1, matrix2), matrix3, path_arc=90 * DEGREES),
        #                       #     FadeOut(all_matrix)
        #                       # )
        #                       )

        self.play(FadeOut(image_prompt, arrow_prompt_embedding, arrow_embedding_model, arrow_model_matrix, prompt))
        self.play(Wiggle(embedding_prompt))
        self.play(FadeOut(embedding_prompt), MoveToTarget(model_diffusion))
        self.play(LaggedStartMap(Create, VGroup(box, line1, line2)))
        # todo: 动画效果不满意
        self.play(
            # Succession(*matrix_mul),
            LaggedStart(
                AnimationGroup(
                    Rotate(gears[i], axis=IN if i == 0 else OUT, about_point=gears[i].get_center())
                    for i in range(3)
                ), run_time=5, lag_ratio=0.0))
        self.wait()

        # 3.2. what is the image
        model_diffusion.generate_target()
        Group(model_diffusion.target, image_prompt).arrange(RIGHT, buff=2)
        arrow_model_image = Arrow(model_diffusion.target.get_right(), image_prompt.get_left())
        image_rgb = Group(
            ImageMobject("assets/prompt_r.png").set(width=4.0).set_opacity(0.8),
            ImageMobject("assets/prompt_g.png").set(width=4.0).set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP),
            ImageMobject("assets/prompt_b.png").set(width=4.0).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP)
        ).move_to(2 * RIGHT)
        image_prompt.generate_target()
        image_prompt.target.move_to(4 * LEFT)
        arrow_images = Arrow(image_prompt.target.get_right(), image_rgb.get_left())

        self.play(FadeOut(box, line1, line2))
        self.play(MoveToTarget(model_diffusion), GrowArrow(arrow_model_image))
        self.play(FadeIn(image_prompt))
        self.wait()
        self.play(FadeOut(model_diffusion, arrow_model_image), MoveToTarget(image_prompt))
        self.play(GrowArrow(arrow_images))
        self.play(LaggedStartMap(FadeIn, image_rgb, shift=LEFT, lag_ratio=1.0))
        self.wait()

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
            faded_line_ratio=0,  # Disable fading of grid lines
        )
        lattice.set(width=4.0)
        lattices = Group(lattice.copy(), lattice.copy(), lattice.copy()).arrange(RIGHT, buff=0.4)
        eq = Text("=").scale(3)
        self.play(FadeOut(image_prompt, arrow_images), MoveToTarget(image_rgb))
        self.play(FadeIn(lattices))
        self.wait()

        image_eq = Group(image_prompt, eq, matrix_image).arrange(RIGHT, buff=0.5)
        self.play(FadeOut(lattices, image_rgb))
        self.play(FadeIn(image_eq))
        self.wait()

        # 4.
        point_papers = VGroup(
            Text("2020.06 \nDDPM", font="menlo"),
            Text("2021.03 \nCLIP", font="menlo"),
            Text("2021.12 \nLatent Diffusion", font="menlo"),
            Text("2024.03 \nStable Diffusion 3", font="menlo"),
        )
        arrow_history = Arrow(7 * LEFT, 7 * RIGHT)
        dots = VGroup(*[Dot(radius=0.1) for _ in range(4)]).arrange(RIGHT, buff=3)
        for dot, point_paper in zip(dots, point_papers):
            point_paper.next_to(dot, direction=UP, buff=0.1).scale(0.4)

        self.play(FadeOut(image_eq))
        self.play(Create(arrow_history))
        self.play(Succession(*[Create(VGroup(dots[i], point_papers[i])) for i in range(4)]))
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
        self.play(Transform(VGroup(point_papers, arrow_history, dots), text_ddpm))
        self.play(FadeIn(model_diffusion))
        self.play(FadeIn(image_noise),
                  GrowArrow(arrow_noise_model),
                  Create(prompt_cat),
                  GrowArrow(arrow_prompt_model),
                  LaggedStart(
                      AnimationGroup(
                          Rotate(gears[i], axis=IN if i == 0 else OUT, about_point=gears[i].get_center())
                          for i in range(3)
                      ), run_time=2, lag_ratio=0.0)
                  )
        self.play(GrowArrow(arrow_model_cat), FadeIn(image_cat))
        self.wait()
        self.play(Indicate(hard))
        self.play(FadeOut(image_noise), FadeIn(image_cat_35))
        self.play(FadeOut(hard), Indicate(easy))

        # 5.1 Decode
        path_cats = (["assets/cat_0.jpg"] + [f"assets/cat_0_00{i}.png" for i in range(35, 96, 5)] +
                     ["assets/cat_0_0999.png"])
        image_cat_decode = Group(
            *[Group(
                *[ImageMobject(path_cats[j]) for j in range(i * 5, (i + 1) * 5)]
            ).set(height=1.8).arrange(LEFT if i != 1 else RIGHT, buff=0.3) for i in range(3)]
        ).arrange(DOWN, buff=0.3).shift(0.5 * DOWN)

        self.play(FadeOut(easy, arrow_model_cat, model_diffusion, arrow_noise_model,
                          image_noise, arrow_prompt_model, prompt_cat),
                  Transform(image_cat_35, image_cat_decode[0][1]),  # Transform只是改变形状
                  Transform(image_cat, image_cat_decode[0][0]))
        arrow_between_images = []
        for i, image_group in enumerate(image_cat_decode):
            j = 0
            time1 = 0.7
            time2 = 0.3
            for j in range(len(image_group) - 1):
                arr = Arrow(image_group[j + 1].get_right(), image_group[j].get_left(),
                            stroke_width=1.0, tip_length=0.1) \
                    if i != 1 else Arrow(image_group[j + 1].get_left(), image_group[j].get_right(),
                                         stroke_width=1.0, tip_length=0.1)
                arrow_between_images.append(arr)
                self.play(FadeIn(image_group[j], run_time=time1 if i == 0 else time2),
                          GrowArrow(arr, run_time=time1 if i == 0 else time2))
            self.play(FadeIn(image_group[j + 1], run_time=time1 if i == 0 else time2))
            if i == 0:
                # todo: 形状不满意
                arr = Arrow(image_cat_decode[i + 1][0].get_left(), image_group[j + 1].get_left(),
                            path_arc=-90 * DEGREES, stroke_width=1.0, tip_length=0.1, buff=0.0)
                arrow_between_images.append(arr)
                self.play(GrowArrow(arr, run_time=time1))
            elif i == 1:
                arr = Arrow(image_cat_decode[i + 1][0].get_right(), image_group[j + 1].get_right(),
                            path_arc=90 * DEGREES, stroke_width=1.0, tip_length=0.1, buff=0.0)
                arrow_between_images.append(arr)
                self.play(GrowArrow(arr, run_time=time2))

        images_and_lines = Group(image_cat_decode, Group(*arrow_between_images))
        images_and_lines.generate_target()
        images_and_lines.target.scale(0.7).to_edge(RIGHT)
        brace_images_and_lines = Brace(images_and_lines.target, direction=LEFT, buff=0.1)
        text_images_and_lines = Text("Decode").next_to(brace_images_and_lines, LEFT)
        self.play(FadeOut(image_cat_35, image_cat))  # 因为用transform，所以还得去掉
        self.play(MoveToTarget(images_and_lines))
        self.play(GrowFromCenter(brace_images_and_lines), Write(text_images_and_lines))

        # 5.2 Encode
        image_text_encode_decode = Group(
            *([ele for i in [f"assets/{f}" for f in ['cat_0.jpg', 'cat_0_0065.png', 'cat_0_0999.png', 'cat_0_0065.png']]
               for ele in [ImageMobject(i).set(height=1.4), Text("···").scale(0.7)]] +
              [ImageMobject("assets/cat_0.jpg").set(height=1.4)]
              )
        ).arrange(RIGHT, buff=0.3)
        # 特殊处理，方便做transform
        image_cat_decode = Group(*[i for group in image_cat_decode for i in group])
        image_encode_decode = Group(*[i for i in image_text_encode_decode if isinstance(i, ImageMobject)])
        text_encode_decode = Group(*[i for i in image_text_encode_decode if isinstance(i, Text)])

        image_text_encode_only = Group(
            *([ele for i in [f"assets/{f}" for f in ['cat_0.jpg', 'cat_0_0040.png', 'cat_0_0060.png', 'cat_0_0080.png']]
               for ele in (ImageMobject(i).set(height=1.4), Text("···").scale(0.7))] +
              [ImageMobject("assets/cat_0_0999.png").set(height=1.4)]
              )
        ).arrange(RIGHT, buff=0.3)

        # image_encode_set = Group(
        #     *[Group(*([ele for j in [f"assets/cat_{i}{f}" for f in ('.jpg', '_0040.png', '_0060.png', '_0080.png')]
        #                for ele in [ImageMobject(j).set(width=2), Text("···").scale(0.5)]] +
        #               [ImageMobject(f"assets/cat_{i}_0999.png").set(width=2)]
        #               )
        #             ).arrange(RIGHT, buff=0.3)
        #       for i in range(1, 4)]
        # ).arrange(DOWN, buff=0.3).to_edge(DOWN)

        formula_encode = MathTex(
            r"\nabla_\theta\left\|\boldsymbol{\epsilon}-\boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t\right)\right\|^2")
        formula_xt = MathTex(r"\mathbf{x}_t=\sqrt{\bar{\alpha}_t} ",
                             r"\mathbf{x}_0",
                             r"+\sqrt{1-\bar{\alpha}_t} ",
                             r"\boldsymbol{\epsilon}")
        formula_decode = MathTex(
            r"\mathbf{x}_{t-1}=\frac{1}{\sqrt{\alpha_t}}\left(\mathbf{x}_t-\frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \boldsymbol{\epsilon}_\theta\left(\mathbf{x}_t, t\right)\right)+\sigma_t \mathbf{z}")
        brace_decode = Brace(image_text_encode_decode[4:], direction=UP, buff=0.1)
        text_decode = Text("Decode").next_to(brace_decode, UP)
        brace_encode = Brace(image_text_encode_decode[:5], direction=DOWN, buff=0.1)
        text_encode = Text("Encode").next_to(brace_encode, DOWN)
        formula_decode.next_to(text_decode, UP)
        brace_encode_only = Brace(image_text_encode_only, direction=DOWN, buff=0.1)
        text_encode_steps = Text("1000 Steps").next_to(brace_encode_only, DOWN)
        formula_xt.next_to(text_encode_steps, DOWN)
        frame_box_xt = SurroundingRectangle(formula_xt[1], corner_radius=0.01).set_stroke(width=2.0)
        frame_box_noise = SurroundingRectangle(formula_xt[3], corner_radius=0.01).set_stroke(width=2.0)
        arrow_xt_image = Arrow(frame_box_xt.get_bottom(), image_text_encode_only[0].get_bottom(),
                               path_arc=-90 * DEGREES, stroke_width=2.0, tip_length=0.2, buff=0.0)

        self.play(FadeOut(brace_images_and_lines, text_images_and_lines, VGroup(*arrow_between_images)))
        self.play(Transform(image_cat_decode, image_encode_decode), FadeIn(text_encode_decode))
        self.play(GrowFromCenter(brace_decode), Write(text_decode))
        self.play(GrowFromCenter(brace_encode), Write(text_encode))
        self.play(FadeOut(brace_decode, text_decode))
        self.play(Transform(image_text_encode_decode, image_text_encode_only),
                  FadeOut(image_cat_decode))
        self.play(Transform(brace_encode, brace_encode_only))
        self.play(Transform(text_encode, text_encode_steps))
        self.play(Write(formula_xt))
        self.play(Create(frame_box_xt), GrowArrow(arrow_xt_image))
        self.play(Create(frame_box_noise))
        # self.play(Write(formula_decode))

        # self.play(FadeOut(formula_xt, brace_encode, image_text_encode_decode, text_encode_steps, text_encode))


if __name__ == "__main__":
    scene = Models()
    scene.render()
