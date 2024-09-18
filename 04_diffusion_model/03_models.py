from utils import *


# 满意
class Models(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        # 3. show generating images
        gear = SVGMobject("assets/wheel.svg")
        image_prompt = ImageMobject("assets/prompt.png").set(width=4.2)
        gears = VGroup(gear.copy().scale(0.5).shift(0.78 * UP).set_color(YELLOW),
                       gear.copy().scale(0.5).shift(0.57 * LEFT).set_color(ORANGE),
                       gear.copy().scale(0.5).shift(0.57 * RIGHT))
        text_model = Text("Diffusion Model", font_size=24, color=GREY).next_to(gears, DOWN, SMALL_BUFF)
        surrounding_model = SurroundingRectangle(VGroup(gears, text_model),
                                                 buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        model_diffusion = VGroup(gears, text_model, surrounding_model).move_to(ORIGIN)

        gears_clip = VGroup(gear.copy().scale(0.5).shift(0.8 * UP).rotate(10 * DEGREES).set_color('#3fc1c9'),
                            gear.copy().scale(0.5).shift(0.55 * RIGHT).rotate(-8 * DEGREES).set_color('#364f6b'))
        text_clip_model = Text("CLIP Model", font_size=24, color=GREY).next_to(gears_clip, DOWN, SMALL_BUFF)
        surrounding_clip = SurroundingRectangle(VGroup(gears_clip, text_clip_model),
                                                buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        model_clip = VGroup(gears_clip, text_clip_model, surrounding_clip).move_to(4 * LEFT + 2 * DOWN)
        self.add(model_diffusion, model_clip)


if __name__ == "__main__":
    scene = Models()
    scene.render()
