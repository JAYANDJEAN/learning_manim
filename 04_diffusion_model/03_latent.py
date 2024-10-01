from utils import *


class LATENT(Diffusion):
    def __init__(self):
        super().__init__()

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
        brace_image_up = BraceLabel(image_cat.target, "1024 pixels", UP, Text, 40)
        brace_image_right = BraceLabel(image_cat.target, "1024 pixels", RIGHT, Text, 40)

        self.play(LaggedStartMap(FadeIn, training_data, lag_ratio=0.5, shift=DOWN))
        self.play(FadeOut(training_data), MoveToTarget(image_cat))
        self.play(GrowFromCenter(brace_image_up))
        self.play(GrowFromCenter(brace_image_right))

        # --------------------------------------------------
        image_big = Group(image_cat, brace_image_up)
        image_big.generate_target()
        image_cat_blurred = ImageMobject("assets/cat_blurred.jpg").set(width=2.0)
        small_brace_image_up = BraceLabel(image_cat_blurred, "64 pixels", UP, Text, 20)
        small_brace_image_right = BraceLabel(image_cat_blurred, "64 pixels", RIGHT, Text, 20)
        image_small = Group(image_cat_blurred, small_brace_image_up, small_brace_image_right)
        Group(image_big.target, image_small).arrange(RIGHT, buff=1.0)

        self.play(
            FadeOut(brace_image_right),
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

        brace_matrix1 = VGroup(
            BraceBetweenPoints(
                matrix_image[3].get_corner(UL),
                matrix_image[0].get_corner(UL), buff=0.1, color=GREY),
            Text("4").scale(0.4).next_to(matrix_image[0].get_corner(UL), LEFT + 1.6 * UP))
        brace_matrix2 = VGroup(
            Brace(matrix_image[0], RIGHT, buff=0.1, color=GREY),
            Text("64").scale(0.4).next_to(matrix_image[0], RIGHT, 0.45)
        )
        brace_matrix3 = VGroup(
            Brace(matrix_image[0], DOWN, buff=0.1, color=GREY),
            Text("64").scale(0.4).next_to(matrix_image[0], DOWN, 0.45)
        )

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
            GrowFromCenter(brace_matrix1),
            GrowFromCenter(brace_matrix2),
            GrowFromCenter(brace_matrix3)
        )
        self.play(
            Rotate(self.gears_vae_decoder[0], axis=IN,
                   about_point=self.gears_vae_decoder[0].get_center()),
            FadeIn(image_cat_copy, shift=DOWN)
        )
        self.play(FadeOut(model_and_image, brace_matrix1, brace_matrix2, brace_matrix3, self.model_vqvae))

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
        text_dim1 = MathTex("4*64*64").scale(0.3).next_to(noise, LEFT)
        text_dim2 = MathTex("4*64*64").scale(0.3).next_to(noise_out, UP)
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
        self.latent1()
        self.latent2()


if __name__ == "__main__":
    LATENT().render()
