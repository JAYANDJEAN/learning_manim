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
        embedding_text_cat = WeightMatrix(length=14).set(width=0.5).move_to(2.5 * RIGHT)
        brace_text = Brace(embedding_text_cat, direction=RIGHT, buff=0.1)
        dim_text = Text("768-dimensional", font_size=24).set_color(YELLOW).next_to(brace_text, RIGHT)
        embedding_text_cat.generate_target()
        embedding_text_cat.target.scale(0.7).move_to(6 * RIGHT + 1 * UP)
        text_cat.generate_target()
        text_cat.target.scale(0.3).next_to(embedding_text_cat.target, UP)

        image_cat = ImageMobject("assets/cat_0.jpg").set(height=2).move_to(3 * LEFT)
        embedding_image = WeightMatrix(length=14).set(width=0.5).move_to(2.5 * RIGHT)
        embedding_image.generate_target()
        embedding_image.target.scale(0.7).move_to(5 * RIGHT + 1 * UP)
        image_cat.generate_target()
        image_cat.target.scale(0.15).next_to(embedding_image.target, UP)

        text_dog = Text("A DOG").scale(0.9)
        surrounding_text_dog = SurroundingRectangle(
            text_dog, buff=0.1, color=WHITE, corner_radius=0.1).set_stroke(width=0.7)
        text_dog = VGroup(text_dog, surrounding_text_dog).move_to(3 * LEFT)
        embedding_text_dog = WeightMatrix(length=14).set(width=0.5).move_to(2.5 * RIGHT)
        embedding_text_dog.generate_target()
        embedding_text_dog.target.scale(0.7).move_to(4 * RIGHT + 1 * UP)
        text_dog.generate_target()
        text_dog.target.scale(0.3).next_to(embedding_text_dog.target, UP)

        all_embedding = VGroup(embedding_text_cat, embedding_image, embedding_text_dog)
        all_label = Group(text_cat, image_cat, text_dog)
        all_embedding.generate_target()
        all_embedding.target.set(width=0.5).arrange(LEFT, buff=0.3).move_to(1.3 * LEFT + 0.3 * DOWN)
        all_label.generate_target()
        for i, label in enumerate(all_label.target):
            label.set(width=0.6).next_to(all_embedding.target[i], UP)
        # surrounding_all = SurroundingRectangle(Group(all_embedding.target, all_label.target),
        #                                        buff=0.1, color=WHITE, corner_radius=0.1).set_stroke(width=0.7)
        # box = Rectangle(width=6, height=4).set_fill(GREY_E, 1).set_stroke(WHITE, 1).move_to(4 * RIGHT).match_y(
        #     surrounding_all)
        # line1 = Line(start=surrounding_all.get_corner(direction=UR),
        #              end=box.get_corner(direction=UL)).set_stroke(WHITE, 1)
        # line2 = Line(start=surrounding_all.get_corner(direction=DR),
        #              end=box.get_corner(direction=DL)).set_stroke(WHITE, 1)

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
        self.play(FadeOut(brace_text, dim_text))
        self.play(MoveToTarget(embedding_text_cat), MoveToTarget(text_cat))

        self.play(FadeIn(image_cat))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(gears_clip[i], axis=IN if i == 0 else OUT, about_point=gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(image_cat, embedding_image, path_arc=-30 * DEGREES))
        )
        self.play(MoveToTarget(embedding_image), MoveToTarget(image_cat))

        self.play(Create(text_dog))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(gears_clip[i], axis=IN if i == 0 else OUT, about_point=gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(text_dog, embedding_text_dog)),
        )
        self.play(MoveToTarget(embedding_text_dog), MoveToTarget(text_dog))
        self.wait()
        self.play(model_clip.animate.shift(4 * LEFT + 0.3 * DOWN),
                  MoveToTarget(all_embedding),
                  MoveToTarget(all_label))
        self.wait()
        self.play(FadeOut(all_embedding, all_label, target_position=4 * RIGHT, scale=0.6))


class CLIPEmbedding(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        text_cat = Text("A CAT").scale(0.1).move_to(2 * LEFT)
        image_cat = ImageMobject("assets/cat_0.jpg").set(height=0.5).move_to(2.1 * LEFT)
        text_dog = Text("A DOG").scale(0.1).move_to(2 * RIGHT, 2 * UP)
        self.add_fixed_in_frame_mobjects(text_cat, text_dog, image_cat)
        axes = ThreeDAxes()
        vector1 = Arrow3D(start=ORIGIN, end=2 * DOWN + 2 * RIGHT + 4 * UP, color=RED)
        vector2 = Arrow3D(start=ORIGIN, end=2.1 * DOWN + 2.1 * RIGHT + 3 * UP, color=GREEN)
        vector3 = Arrow3D(start=ORIGIN, end=2 * UP + 2 * LEFT + 3 * UP, color=BLUE)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES, focal_distance=20.0)
        self.play(Create(axes))
        self.play(Create(vector1), Write(text_cat))
        self.play(Create(vector2), FadeIn(image_cat))
        self.play(Create(vector3), Write(text_dog))
        # self.begin_ambient_camera_rotation(rate=0.05)  # 以一定速度旋转相机
        # self.stop_ambient_camera_rotation()
        self.wait(2)


if __name__ == "__main__":
    scene = CLIPEmbedding()
    scene.render()
