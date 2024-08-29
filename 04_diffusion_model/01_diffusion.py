from utils import *


class Models(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        gear = SVGMobject("assets/wheel.svg")
        image_out = ImageMobject("assets/prompt.png").set(width=4.2)

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
        matrix = VGroup(matrix3, matrix2, matrix1)

        text_prompt = Paragraph("a cyberpunk with ",
                                "natural greys and ",
                                "whites and browns.",
                                line_spacing=1.0, font="menlo").scale(0.4)
        surrounding_prompt = SurroundingRectangle(text_prompt,
                                                  buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        prompt = VGroup(surrounding_prompt, text_prompt)

        Group(prompt, embedding, model, matrix).arrange(RIGHT, buff=1.0)
        gears_rotate = AnimationGroup(
            Rotate(gears[0], axis=IN, about_point=gears[0].get_center()),
            Rotate(gears[1], about_point=gears[1].get_center()),
            Rotate(gears[2], about_point=gears[2].get_center())
        )
        arrow1 = Arrow(prompt.get_right(), embedding.get_left())
        arrow2 = Arrow(embedding.get_right(), model.get_left())
        arrow3 = Arrow(model.get_right(), matrix.get_left())
        image_out.move_to(matrix.get_center())

        self.play(FadeOut(models), FadeIn(model))
        self.play(Write(text_prompt, run_time=3))
        self.play(Create(surrounding_prompt))
        self.play(Create(arrow1), Create(embedding))
        self.play(Create(arrow2), LaggedStart(gears_rotate, run_time=4, lag_ratio=0.0))
        self.play(Create(arrow3), Create(matrix))
        self.wait()
        self.play(FadeOut(matrix), FadeIn(image_out))
        self.wait()

        # 4. why we need embedding
        model_copy = model.copy()
        box = Rectangle(width=8.0, height=5.0).set_fill(GREY_E, 1).set_stroke(WHITE, 1)
        VGroup(model_copy, box).arrange(RIGHT, buff=1.5)
        line1 = Line(start=model_copy.get_corner(direction=UR), end=box.get_corner(direction=UL)).set_stroke(WHITE, 1)
        line2 = Line(start=model_copy.get_corner(direction=DR), end=box.get_corner(direction=DL)).set_stroke(WHITE, 1)

        self.play(FadeOut(matrix, image_out, arrow1, arrow2, arrow3, prompt))
        self.play(Wiggle(embedding))
        self.play(FadeOut(embedding), model.animate.move_to(model_copy.get_center()))
        self.play(LaggedStartMap(Create, VGroup(box, line1, line2)))
        self.wait()

        # 5.


if __name__ == "__main__":
    scene = Models()
    scene.render()
