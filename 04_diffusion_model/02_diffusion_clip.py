from manim import *
from utils import *


class CLIP(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        gear = SVGMobject("assets/wheel.svg")
        # CLIP
        text_clip = Text("CLIP", font="menlo").to_edge(UL, buff=0.5).scale(0.7)

        gears_clip = VGroup(gear.copy().scale(0.5).shift(0.8 * UP).rotate(10 * DEGREES).set_color('#3fc1c9'),
                            gear.copy().scale(0.5).shift(0.55 * RIGHT).rotate(-8 * DEGREES).set_color('#364f6b'))
        text_clip_model = Text("CLIP Model", font_size=24, color=GREY).next_to(gears_clip, DOWN, SMALL_BUFF)
        surrounding_clip = SurroundingRectangle(VGroup(gears_clip, text_clip_model),
                                                buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        model_clip = VGroup(gears_clip, text_clip_model, surrounding_clip).move_to(ORIGIN)

        text_cat = Text("A CAT").scale(0.9)
        surrounding_text_cat = SurroundingRectangle(
            text_cat, buff=0.1, color=WHITE, corner_radius=0.1).set_stroke(width=0.7)
        text_cat = VGroup(text_cat, surrounding_text_cat).move_to(3 * LEFT)
        embedding_text_cat = WeightMatrix(length=12).set(width=0.5).move_to(3 * RIGHT + 1 * UP)
        brace_text = Brace(embedding_text_cat, direction=RIGHT, buff=0.1)
        dim_text = Text("768-dimensional", font_size=24).set_color(YELLOW).next_to(brace_text, RIGHT)

        text_dog = Text("A DOG").scale(0.9)
        surrounding_text_dog = SurroundingRectangle(
            text_dog, buff=0.1, color=WHITE, corner_radius=0.1).set_stroke(width=0.7)
        text_dog = VGroup(text_dog, surrounding_text_dog).move_to(3 * LEFT)
        embedding_text_dog = WeightMatrix(length=14).set(width=0.5).move_to(3.5 * RIGHT)

        image_cat = ImageMobject("assets/cat_0.jpg").set(height=2).move_to(3 * LEFT)
        embedding_image = WeightMatrix(length=12).set(width=0.5).move_to(4 * RIGHT + 1 * DOWN)

        model_clip_embedding = VGroup(model_clip, embedding_text_cat, embedding_image, embedding_text_dog)

        self.add(text_clip)
        self.play(FadeIn(model_clip))
        self.play(Create(text_cat))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(gears_clip[i], axis=IN if i == 0 else OUT, about_point=gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(text_cat, embedding_text_cat))
        )
        self.play(GrowFromCenter(brace_text), Create(dim_text))
        self.play(
            FadeOut(brace_text, dim_text),
            text_cat.animate.scale(0.5).next_to(embedding_text_cat, RIGHT)
        )
        self.play(Create(text_dog))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(gears_clip[i], axis=IN if i == 0 else OUT, about_point=gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(text_dog, embedding_text_dog)),
        )
        self.play(text_dog.animate.scale(0.5).next_to(embedding_text_dog, RIGHT))
        self.play(FadeIn(image_cat))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(gears_clip[i], axis=IN if i == 0 else OUT, about_point=gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(image_cat, embedding_image, path_arc=-30 * DEGREES))
        )
        self.play(image_cat.animate.scale(0.2).next_to(embedding_image, RIGHT))
        self.wait(2)
        self.play(model_clip_embedding.animate.shift(3 * LEFT))
        self.wait(2)

        axes_3d = ThreeDAxes(x_range=(-4, 4, 1), y_range=(-4, 4, 1), z_range=(-4, 4, 1))
        vector1 = Vector((1, 2, 3), color=RED)
        vector2 = Vector((-1, -1, 2), color=GREEN)
        vector3 = Vector((2, -2, -1), color=BLUE)
        d = VGroup(axes_3d, vector1, vector2, vector3).rotate(-45, RIGHT, ORIGIN).rotate(-45, IN, ORIGIN).rotate(-45, UP, ORIGIN)
        self.add(d)
        self.wait(2)


if __name__ == "__main__":
    scene = CLIP()
    scene.render()
