from utils import *


class Models(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        gear = SVGMobject("assets/wheel.svg")
        image_prompt = ImageMobject("assets/prompt.png").set(width=4.2)

        # 1. title
        title = Text("How does diffusion model work")
        self.play(Write(title), run_time=2)
        logo = MathTex(r"\mathbb{JAYANDJEAN}",
                       fill_color="#ece6e2").next_to(title, DOWN, buff=0.5).scale(1.2)
        self.play(Write(logo), run_time=1)
        self.play(FadeOut(title),
                  logo.animate.scale(0.4).move_to(RIGHT * 5.5 + UP * 3.5))

        # 2. show diffusion products
        mid = ImageMobject("assets/mid.jpg").set(height=2)
        sd3 = ImageMobject("assets/sd3.png").set(height=2)
        flux = ImageMobject("assets/flux.png").set(height=2)
        models = Group(mid, sd3, flux).arrange(RIGHT, buff=0.2).align_to(LEFT)
        self.play(LaggedStartMap(FadeIn, models, lag_ratio=1.0, run_time=3))
        self.wait()

        # 3. show generating images
        gears = VGroup(gear.copy().scale(0.5).shift(0.78 * UP).set_color(YELLOW),
                       gear.copy().scale(0.5).shift(0.57 * LEFT).set_color(ORANGE),
                       gear.copy().scale(0.5).shift(0.57 * RIGHT))

        text_model = Text("Diffusion Model", font_size=24, color=GREY).next_to(gears, DOWN, SMALL_BUFF)
        surrounding_model = SurroundingRectangle(VGroup(gears, text_model), buff=0.2, color=WHITE, corner_radius=0.3)
        surrounding_model.set_stroke(width=0.5)
        model = VGroup(gears, text_model, surrounding_model)

        embedding = WeightMatrix(length=15).set(width=0.5)
        matrix1 = WeightMatrix(shape=(12, 7)).set(width=4)
        matrix2 = WeightMatrix(shape=(12, 7)).set(width=4).set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP)
        matrix3 = WeightMatrix(shape=(12, 7)).set(width=4).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP)
        matrix_image = VGroup(matrix3, matrix2, matrix1)

        text_prompt = Paragraph("a cyberpunk with ",
                                "natural greys and ",
                                "whites and browns.",
                                line_spacing=1.0, font="menlo").scale(0.4)
        surrounding_prompt = SurroundingRectangle(text_prompt,
                                                  buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        prompt = VGroup(surrounding_prompt, text_prompt)

        Group(prompt, embedding, model, matrix_image).arrange(RIGHT, buff=1.0)
        gears_rotate = AnimationGroup(
            Rotate(gears[0], axis=IN, about_point=gears[0].get_center()),
            Rotate(gears[1], about_point=gears[1].get_center()),
            Rotate(gears[2], about_point=gears[2].get_center())
        )
        arrow1 = Arrow(prompt.get_right(), embedding.get_left())
        arrow2 = Arrow(embedding.get_right(), model.get_left())
        arrow3 = Arrow(model.get_right(), matrix_image.get_left())
        image_prompt.move_to(matrix_image.get_center())

        self.play(FadeOut(models), FadeIn(model))
        self.play(Write(text_prompt))
        self.play(Create(surrounding_prompt))
        self.play(Create(arrow1), Create(embedding))
        self.play(Create(arrow2), LaggedStart(gears_rotate, run_time=3, lag_ratio=0.0))
        self.play(Create(arrow3), Create(matrix_image))
        self.wait()
        self.play(FadeOut(matrix_image), FadeIn(image_prompt))
        self.wait()

        # 3.1. why we need embedding
        model_copy = model.copy()
        box = Rectangle(width=9.5, height=4.5).set_fill(GREY_E, 1).set_stroke(WHITE, 1)
        VGroup(model_copy, box).arrange(RIGHT, buff=1)
        line1 = Line(start=model_copy.get_corner(direction=UR), end=box.get_corner(direction=UL)).set_stroke(WHITE, 1)
        line2 = Line(start=model_copy.get_corner(direction=DR), end=box.get_corner(direction=DL)).set_stroke(WHITE, 1)

        self.play(FadeOut(matrix_image, image_prompt, arrow1, arrow2, arrow3, prompt))
        self.play(Wiggle(embedding))
        self.play(FadeOut(embedding), model.animate.move_to(model_copy.get_center()))
        self.play(LaggedStartMap(Create, VGroup(box, line1, line2)))

        shape_list = [[(7, 7), (7, 6), (7, 6)],
                      [(8, 6), (6, 6), (8, 6)],
                      [(8, 5), (5, 6), (8, 6)],
                      [(7, 7), (7, 6), (7, 6)],
                      [(8, 6), (6, 6), (8, 6)],
                      ]
        all_matrix = None
        for i, shapes in enumerate(shape_list):
            matrix1, matrix2, matrix3 = [
                VGroup(WeightMatrix(shape=shape).set(width=0.4 * shape[1]),
                       WeightMatrix(shape=shape).set(width=0.4 * shape[1])
                       .set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP),
                       WeightMatrix(shape=shape).set(width=0.4 * shape[1])
                       .set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP)
                       ) for shape in shapes]
            eq = Tex('=')
            all_matrix = (VGroup(matrix1, matrix2, eq, matrix3)
                          .arrange(RIGHT, buff=0.2)
                          .move_to(box.get_center()))
            two_matrix = VGroup(matrix1.copy(), matrix2.copy())
            self.play(Create(matrix1), Create(matrix2), Create(eq))
            # todo：不满意
            self.play(FadeOut(two_matrix, target_position=matrix3.get_center(), scale=0.5))
            self.add(matrix3)
            if i != len(shape_list) - 1:
                self.play(FadeOut(all_matrix))
        self.wait()

        # 3.2. what is the image
        model_copy = model.copy()
        Group(model_copy, image_prompt).arrange(RIGHT, buff=2)
        arrow_model_image = Arrow(model_copy.get_right(), image_prompt.get_left())
        image_rgb = Group(
            ImageMobject("assets/prompt_r.png").set(width=4.0).set_opacity(0.8),
            ImageMobject("assets/prompt_g.png").set(width=4.0).set_opacity(0.4).shift(0.1 * RIGHT + 0.1 * UP),
            ImageMobject("assets/prompt_b.png").set(width=4.0).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP)
        ).move_to(2 * RIGHT)
        self.play(FadeOut(box, line1, line2, all_matrix))
        self.play(model.animate.move_to(model_copy.get_center()), Create(arrow_model_image))
        self.play(FadeIn(image_prompt))
        self.wait()
        self.play(FadeOut(model, arrow_model_image), image_prompt.animate.move_to(4 * LEFT))
        arrow_images = Arrow(image_prompt.get_right(), image_rgb.get_left())
        self.play(Create(arrow_images))
        self.play(FadeOut(image_prompt.copy(), target_position=image_rgb.get_center()),
                  FadeIn(image_rgb))
        self.wait()

        image_rgb_copy = image_rgb.copy()
        image_rgb_copy.arrange(RIGHT, buff=0.4).set(opacity=1.0)
        lattice = NumberPlane(
            x_range=(-14, 14, 1),
            y_range=(-17, 17, 1),
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 2,
                "stroke_opacity": 1,
            },
            axis_config={
                "stroke_color": GRAY,
                "stroke_width": 2,
                "include_numbers": False,
            },
            faded_line_ratio=0,  # Disable fading of grid lines
        )
        lattice.set(width=4.0)
        lattices = Group(lattice.copy(), lattice.copy(), lattice.copy()).arrange(RIGHT, buff=0.4)
        self.play(FadeOut(image_prompt, arrow_images), Transform(image_rgb, image_rgb_copy))
        self.play(FadeIn(lattices))
        self.wait()

        eq = Text("=").scale(3)
        image_eq = Group(image_prompt, eq, matrix_image).arrange(RIGHT, buff=0.5)
        self.play(FadeOut(lattices, image_rgb))
        self.play(FadeIn(image_eq))
        self.wait()

        # 4.
        point_papers = [
            Text("2020.06 \nDDPM", font="menlo"),
            Text("2021.03 \nCLIP", font="menlo"),
            Text("2021.12 \nLatent Diffusion", font="menlo"),
            Text("2024.03 \nStable Diffusion 3", font="menlo"),
        ]
        papers_name = [
            Text("Denoising Diffusion Probabilistic Models", font="menlo"),
            Text("Learning Transferable Visual Models \nFrom Natural Language Supervision", font="menlo"),
            Text("High-Resolution Image Synthesis \nwith Latent Diffusion Models", font="menlo"),
            Text("Scaling Rectified Flow Transformers \nfor High-Resolution Image Synthesis", font="menlo"),
        ]
        arrow_history = Arrow(7 * LEFT, 7 * RIGHT)
        dots = VGroup(*[Dot(radius=0.1) for _ in range(4)]).arrange(RIGHT, buff=3.1)
        for dot, point_paper, paper in zip(dots, point_papers, papers_name):
            point_paper.next_to(dot, direction=UP, buff=0.2).scale(0.4)
            paper.next_to(dot, direction=DOWN, buff=0.2).scale(0.2)

        self.play(FadeOut(image_eq))
        self.play(Create(arrow_history))
        self.play(Create(dots[0]), Write(point_papers[0]))
        self.play(Write(papers_name[0]))
        self.play(Create(dots[1]), Write(point_papers[1]))
        self.play(Write(papers_name[1]))
        self.play(Create(dots[2]), Write(point_papers[2]))
        self.play(Write(papers_name[2]))
        self.play(Create(dots[3]), Write(point_papers[3]))
        self.play(Write(papers_name[3]))
        self.wait()






if __name__ == "__main__":
    scene = Models()
    scene.render()
