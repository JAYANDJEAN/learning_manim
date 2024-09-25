from utils import *


class LATENT(Diffusion):
    def __init__(self):
        super().__init__()

    def latent1(self):
        image_cat = ImageMobject("assets/cat.jpg").set(width=3)
        text_cat = Text("a photo of a cat", font='Menlo', font_size=16).next_to(image_cat, DOWN, buff=0.2)
        image_dog = ImageMobject("assets/dog.jpg").set(width=3)
        text_dog = Text("a photo of a dog", font='Menlo', font_size=16).next_to(image_dog, DOWN, buff=0.2)
        text_left = Text("···")
        data = Group(Group(image_cat, text_cat), Group(image_dog, text_dog), text_left).arrange(RIGHT, buff=0.5)
        image_cat.generate_target()
        image_cat.target.set(width=4.5).move_to(ORIGIN)
        brace_image_up = Brace(image_cat.target, UP, buff=0.2)
        text_pixel1 = Text("1024 pixels", font_size=36).next_to(brace_image_up, UP)
        brace_image_right = Brace(image_cat.target, RIGHT, buff=0.2)
        text_pixel2 = Text("1024 pixels", font_size=36).next_to(brace_image_right, RIGHT)

        self.play(FadeIn(data))
        self.play(FadeOut(text_cat, image_dog, text_dog, text_left), MoveToTarget(image_cat))
        self.play(GrowFromCenter(brace_image_up), Write(text_pixel1))
        self.play(GrowFromCenter(brace_image_right), Write(text_pixel2))

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

        self.model_vqvae.move_to(2 * UP)
        matrix_image = VGroup(
            WeightMatrix(shape=(14, 8)).set(width=2),
            WeightMatrix(shape=(14, 8)).set(width=2).set_opacity(0.3).shift(0.1 * RIGHT + 0.1 * UP),
            WeightMatrix(shape=(14, 8)).set(width=2).set_opacity(0.2).shift(0.2 * RIGHT + 0.2 * UP),
            WeightMatrix(shape=(14, 8)).set(width=2).set_opacity(0.1).shift(0.3 * RIGHT + 0.3 * UP),
        )
        image_cat.set(width=3)
        image_cat_copy = image_cat.copy()
        all = Group(
            image_cat, self.model_vgvae_encoder,
            matrix_image, self.model_vgvae_decoder, image_cat_copy
        ).arrange(RIGHT, buff=0.5).shift(DOWN)
        self.play(FadeIn(self.model_vqvae))
        self.play(FadeIn(all))

        self.wait()

    def latent2(self):
        # def dash_updater(mob):
        #     offset = vt.get_value()
        #     mob['dashes'].become(mob.dash_objects(num_dashes, dash_ratio=0.5, offset=offset))

        self.model_diffusion.move_to(ORIGIN)

        text_scheduler = VGroup(
            Text("Scheduler", color=GREY, font_size=30, font='Menlo'),
            SurroundingRectangle(
                Text("Scheduler", color=GREY, font_size=30, font='Menlo'),
                buff=0.2, color=GREY, corner_radius=0.3, stroke_width=2.0
            )
        ).move_to(3 * UP)
        image_prompt = ImageMobject("assets/prompt.png").set(width=2).move_to(2 * DOWN + 5 * RIGHT)
        embedding_prompt = WeightMatrix(length=15).set(width=0.4)
        prompts = Group(
            self.prompt.scale(0.6), self.model_clip.scale(0.6), embedding_prompt
        ).arrange(RIGHT, buff=0.5)
        prompts.move_to(2 * DOWN + 4.5 * LEFT)
        noise = Prism(dimensions=(1, 1, 0.3)).rotate(-PI / 2).move_to(2 * UP + 5 * LEFT)
        self.model_vae_decoder.scale(0.7).move_to(2 * DOWN + 3 * RIGHT)

        curve = VMobject()
        curve.start_new_path(self.model_diffusion.get_right())
        curve.add_line_to(self.model_diffusion.get_right() + 2.0 * RIGHT)
        curve.add_cubic_bezier_curve_to(
            self.model_diffusion.get_right() + 2.5 * RIGHT,
            self.model_diffusion.get_right() + 2.5 * RIGHT,
            self.model_diffusion.get_right() + 2.5 * RIGHT + 0.5 * UP,
        )
        curve.add_line_to(self.model_diffusion.get_right() + 2.5 * RIGHT + 2 * UP)
        curve.add_cubic_bezier_curve_to(
            self.model_diffusion.get_right() + 2.5 * RIGHT + 2.5 * UP,
            self.model_diffusion.get_right() + 2.5 * RIGHT + 2.5 * UP,
            self.model_diffusion.get_right() + 2.0 * RIGHT + 2.5 * UP,
        )
        curve.add_line_to(self.model_diffusion.get_left() + 2.0 * LEFT + 2.5 * UP)
        curve.add_cubic_bezier_curve_to(
            self.model_diffusion.get_left() + 2.5 * LEFT + 2.5 * UP,
            self.model_diffusion.get_left() + 2.5 * LEFT + 2.5 * UP,
            self.model_diffusion.get_left() + 2.5 * LEFT + 2.0 * UP,
        )
        curve.add_line_to(self.model_diffusion.get_left() + 2.5 * LEFT + 0.5 * UP)
        curve.add_cubic_bezier_curve_to(
            self.model_diffusion.get_left() + 2.5 * LEFT,
            self.model_diffusion.get_left() + 2.5 * LEFT,
            self.model_diffusion.get_left() + 2.0 * LEFT,
        )
        curve.add_line_to(self.model_diffusion.get_left())
        self.add(self.model_diffusion, image_prompt, prompts, noise,
                 self.model_vae_decoder, text_scheduler, curve)

        # vt = ValueTracker(0)
        # num_dashes = 50
        # speed = 7
        #
        # dash1 = DashedMObject(curve, num_dashes=num_dashes, dashed_ratio=0.5, dash_offset=0)
        # dash1.add_updater(dash_updater)
        #
        #
        # self.play(vt.animate.set_value(speed), run_time=5, rate_func=linear)
        # self.wait()

    def construct(self):
        self.camera.background_color = "#1C1C1C"
        self.latent1()
        self.latent2()


if __name__ == "__main__":
    LATENT().render()
