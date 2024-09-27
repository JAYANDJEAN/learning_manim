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
        self.unet.scale(0.5).next_to(formula_encode, DOWN, buff=0.5)
        self.play(GrowFromCenter(brace_embedding), Write(formula_encode))
        self.play(FadeIn(self.unet, shift=RIGHT))
        self.play(
            FadeOut(brace_embedding, formula_encode, training_data_embedding),
            self.unet.animate.move_to(ORIGIN)
        )
        self.wait()

    def latent2(self):
        self.model_text_encoder.move_to(5.5 * LEFT + 1.5 * DOWN)
        self.model_vae_decoder.move_to(4.2 * RIGHT + 1.5 * DOWN)
        embedding_prompt = WeightMatrix(length=15).set(width=0.3).next_to(self.model_text_encoder, RIGHT, buff=0.5)
        image_prompt = ImageMobject("assets/prompt.png").set(width=1.7).next_to(self.model_vae_decoder, RIGHT)
        self.prompt.scale(0.7).next_to(self.model_text_encoder, DOWN, buff=0.5)
        self.unet.scale(0.5).move_to(ORIGIN)
        line_embedding = Arrow(
            embedding_prompt.get_right() + 0.2 * LEFT, embedding_prompt.get_right() + 7.5 * RIGHT,
            color=GREY, stroke_width=2.0, tip_length=0.2,
            max_tip_length_to_length_ratio=1.0,
            max_stroke_width_to_length_ratio=20
        )
        rate_list = [0.75, 0.5, 0.3, 1 / 9, 0.3, 0.5, 0.75]
        delta = 0.1
        line_embedding_unet = VGroup()
        for i, prisms in enumerate(self.unet[0]):
            for p in prisms:
                p_end = (p.get_left() - p.get_center()) * rate_list[i] + p.get_bottom()
                p_start = (p_end[0] - delta) * RIGHT + line_embedding.get_right()[1] * UP
                line_embedding_unet.add(Line(p_start, p_end, color=GREY, stroke_width=2.0))

        line_vae_decode = CubicBezier(
            self.unet.get_right() + 0.2 * LEFT + 0.1 * DOWN,
            self.unet.get_right() + 0.2 * LEFT + 1.0 * DOWN,
            self.unet.get_right() + 0.2 * LEFT + 1.4 * DOWN,
            self.model_vae_decoder.get_left()
        ).set_stroke(GREY, 2.0)

        prism_start = self.unet[0][-1][-1]
        point_start = (prism_start.get_right() - prism_start.get_center()) * 0.75 + prism_start.get_top()
        prism_end = self.unet[0][0][0]
        point_end = (prism_end.get_right() - prism_end.get_center()) * 0.75 + prism_end.get_top()

        text_scheduler = VGroup(
            Text("Scheduler", color=GREY, font='Menlo').scale(0.3),
            SurroundingRectangle(
                Text("Scheduler", color=GREY, font='Menlo').scale(0.3),
                buff=0.07, color=GREY, corner_radius=0.05, stroke_width=2.0
            )
        ).move_to((point_start + point_end) / 2 + 1.5 * UP)

        line_back1 = CubicBezier(
            point_start,
            point_start[0] * RIGHT + 1 * RIGHT + text_scheduler.get_right()[1] * UP + 0.5 * DOWN,
            point_start[0] * RIGHT + 0.5 * RIGHT + text_scheduler.get_right()[1] * UP + 0.1 * DOWN,
            text_scheduler.get_right()
        ).set_stroke(GREY, 2.0)

        line_back2 = CubicBezier(
            point_end,
            point_end[0] * RIGHT + 1 * LEFT + text_scheduler.get_right()[1] * UP + 0.5 * DOWN,
            point_end[0] * RIGHT + 0.5 * LEFT + text_scheduler.get_right()[1] * UP + 0.1 * DOWN,
            text_scheduler.get_left()
        ).set_stroke(GREY, 2.0)

        self.add(
            self.unet, self.prompt, self.model_text_encoder, self.model_vae_decoder,
            embedding_prompt, line_embedding, line_embedding_unet, text_scheduler, image_prompt,
            line_vae_decode, line_back1, line_back2

        )

    def construct(self):
        self.camera.background_color = "#1C1C1C"
        # self.latent1()
        self.latent2()


if __name__ == "__main__":
    LATENT().render()
