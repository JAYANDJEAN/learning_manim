from manim import *


class Models(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        gear = SVGMobject("assets/wheel.svg")
        image_out = ImageMobject("assets/prompt_0.png").set(height=5)

        # 1. title
        title = Text("How does diffusion model works")
        self.play(Write(title), run_time=2)
        logo = MathTex(r"\mathbb{JAYANDJEAN}",
                       fill_color="#ece6e2").next_to(title, DOWN, buff=0.5).scale(1.2)
        self.play(Write(logo), run_time=1)
        self.play(FadeOut(title),
                  logo.animate.scale(0.4).move_to(RIGHT * 5.5 + UP * 3.5))

        # 2. show generating images
        gears = VGroup(gear.copy().scale(0.5).shift(0.78 * UP).set_color(YELLOW),
                       gear.copy().scale(0.5).shift(0.57 * LEFT).set_color(ORANGE),
                       gear.copy().scale(0.5).shift(0.57 * RIGHT))

        text_model = Text("Diffusion Model", font_size=24, color=GREY).next_to(gears, DOWN, SMALL_BUFF)
        surrounding_model = SurroundingRectangle(VGroup(gears, text_model), buff=0.2, color=WHITE, corner_radius=0.3)
        surrounding_model.set_stroke(width=0.5)
        model = VGroup(gears, text_model, surrounding_model)

        text_prompt = Paragraph("a cyberpunk with natural ",
                                "greys and whites and browns",
                                line_spacing=1.0, font="menlo").scale(0.3)
        surrounding_prompt = SurroundingRectangle(text_prompt, buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(
            width=0.5)

        prompt = VGroup(surrounding_prompt, text_prompt)
        Group(prompt, model, image_out).arrange(RIGHT, buff=1.2)
        gears_rotate = AnimationGroup(
            Rotate(gears[0], axis=IN, about_point=gears[0].get_center()),
            Rotate(gears[1], about_point=gears[1].get_center()),
            Rotate(gears[2], about_point=gears[2].get_center())
        )
        arrow1 = Arrow(prompt.get_right(), model.get_left())
        arrow2 = Arrow(model.get_right(), image_out.get_left())

        self.add(model)
        self.play(Write(text_prompt, run_time=3))
        self.play(Create(surrounding_prompt))
        self.play(Create(arrow1))
        self.play(LaggedStart(gears_rotate, run_time=3, lag_ratio=0.0))
        self.play(Create(arrow2))
        self.play(FadeIn(image_out))
        self.wait()

        # 3.
        model_copy = model.copy()
        mid = ImageMobject("assets/mid.jpg").set(height=2)
        sd3 = ImageMobject("assets/sd3.png").set(height=2)
        flux = ImageMobject("assets/flux.png").set(height=2)

        models = Group(mid, sd3, flux).arrange(DOWN, buff=0.2).align_to(LEFT)
        brace_models = Brace(models, direction=LEFT)
        Group(model_copy, brace_models, models).arrange(RIGHT, buff=0.7)

        self.play(FadeOut(arrow1, arrow2, prompt, image_out),
                  Transform(model, model_copy))
        self.play(Create(brace_models))
        self.play(LaggedStartMap(FadeIn, models, lag_ratio=1.0, run_time=3))
        self.wait()



if __name__ == "__main__":
    scene = Models()
    scene.render()
