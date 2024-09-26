from utils import *


class Models(Diffusion):
    def __init__(self):
        super().__init__()

    def construct(self):
        self.camera.background_color = "#1C1C1C"
        # self.model_diffusion.move_to(ORIGIN)
        # self.model_clip.move_to(5 * LEFT + 2 * DOWN)
        # self.model_text_encoder.move_to(2.5 * LEFT + 1 * DOWN)
        # self.model_image_encoder.move_to(2.5 * LEFT + 3 * DOWN)
        # self.model_vqvae.move_to(4 * RIGHT + 2 * DOWN)
        # self.model_vae_encoder.next_to(self.model_vqvae, LEFT)
        # self.model_vae_decoder.next_to(self.model_vqvae, RIGHT)
        # self.unet.scale(0.5).next_to(self.model_diffusion, UP)
        # self.add(
        #     self.model_diffusion, self.model_clip, self.model_text_encoder, self.model_image_encoder,
        #     self.model_vqvae, self.model_vae_encoder, self.model_vae_decoder, self.unet
        # )

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


if __name__ == "__main__":
    Models().render()
