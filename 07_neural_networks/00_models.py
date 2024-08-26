from manim import *


class Models(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        gear = SVGMobject("assets/wheel.svg")
        image_out = ImageMobject("assets/prompt_out.png").set(height=5)

        gears = VGroup(gear.copy().scale(0.5).shift(0.78 * UP).set_color(YELLOW),
                       gear.copy().scale(0.5).shift(0.57 * LEFT).set_color(ORANGE),
                       gear.copy().scale(0.5).shift(0.57 * RIGHT))

        text_model = Text("Deep Learning Model", font_size=24, color=GREY).next_to(gears, DOWN, SMALL_BUFF)
        surrounding_model = SurroundingRectangle(VGroup(gears, text_model), buff=0.2, color=WHITE, corner_radius=0.3)
        surrounding_model.set_stroke(width=0.5)
        model = VGroup(gears, text_model, surrounding_model)

        text_prompt = Text("panel grid, various drawings, "
                           "\nby jean giraud moebius, "
                           "\nblack white, fine line, "
                           "\nsimple line, hatches. ").scale(0.34)
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
        self.wait()
        self.play(Create(prompt))
        self.play(Create(arrow1))
        self.play(LaggedStart(gears_rotate, run_time=3, lag_ratio=0.0))
        self.play(Create(arrow2))
        self.play(FadeIn(image_out))
        self.wait()


if __name__ == "__main__":
    scene = Models()
    scene.render()
