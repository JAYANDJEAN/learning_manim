from utils import *


class SD3(Diffusion):
    def __init__(self):
        super().__init__()

    def sd3(self):
        # -----------------模型--------------------
        noise = SVGMobject("assets/prism0.svg").scale(1.4)
        data_input = VGroup(
            VGroup(
                RoundedRectangle(
                    corner_radius=0.1, height=0.8, width=1.2, stroke_width=0.0
                ).set_fill(ORANGE, 1.0),
                MathTex(r"4096*1536").scale(0.4)
            ),
            VGroup(
                RoundedRectangle(
                    corner_radius=0.1, height=0.45, width=1.2, stroke_width=0.0
                ).set_fill(ORANGE, 1.0),
                MathTex(r"154*1536").scale(0.4)
            )
        ).arrange(DOWN, buff=0.5).next_to(noise, RIGHT)
        mmdit = RoundedRectangle(
            corner_radius=0.1, height=2.8, width=0.3, stroke_width=0.0
        ).set_fill(BLUE_E, 1.0)
        mmdit.z_index = 1

        transformer = VGroup(
            VGroup(
                data_input.copy(),
                mmdit.copy(),
                data_input.copy(),
                mmdit.copy()
            ).arrange(RIGHT, buff=0.2),
            Text("······").set_color(GREY).scale(0.7),
            VGroup(
                data_input.copy(),
                mmdit.copy(),
                data_input.copy()
            ).arrange(RIGHT, buff=0.2)
        ).arrange(RIGHT, buff=0.5).scale(0.8)
        transformer[2][2][1].set_opacity(0.0)
        flow = VGroup(noise.copy(), transformer, noise.copy()).arrange(RIGHT, buff=0.3).move_to(0.6 * UP)
        text_cross = Text("MMDiT Block with Cross Attention").scale(0.4).next_to(flow, UP, buff=0.5)
        line_mmdit_text = VGroup(
            CubicBezier(
                text_cross.get_bottom() + 0.1 * DOWN,
                text_cross.get_bottom() + 0.5 * DOWN,
                flow[1][0][1].get_top() + 0.5 * UP,
                flow[1][0][1].get_top()
            ).set_stroke(GREY, 2.0),
            CubicBezier(
                text_cross.get_bottom() + 0.1 * DOWN,
                text_cross.get_bottom() + 0.5 * DOWN,
                flow[1][0][3].get_top() + 0.5 * UP,
                flow[1][0][3].get_top()
            ).set_stroke(GREY, 2.0),
            CubicBezier(
                text_cross.get_bottom() + 0.1 * DOWN,
                text_cross.get_bottom() + 0.5 * DOWN,
                flow[1][2][1].get_top() + 0.5 * UP,
                flow[1][2][1].get_top()
            ).set_stroke(GREY, 2.0)
        )

        lines_in_flow = VGroup(
            CubicBezier(
                flow[0].get_center() + 0.1 * RIGHT,
                np.array([flow[0].get_center()[0] + 0.1, flow[1][0][0][0].get_center()[1] - 0.1, 0]),
                np.array([flow[0].get_center()[0] + 0.2, flow[1][0][0][0].get_center()[1], 0]),
                flow[1][0][0][0].get_left()
            ).set_stroke(GREY, 2.0),
            Line(flow[1][0][0][0].get_right(), flow[1][0][2][0].get_left()).set_stroke(GREY, 2.0),  # 1
            DashedLine(flow[1][0][2][0].get_right(), flow[1][2][0][0].get_left()).set_stroke(GREY, 2.0),  # 2
            Line(flow[1][2][0][0].get_right(), flow[1][2][2][0].get_left()).set_stroke(GREY, 2.0),  # 3
            Line(flow[1][0][0][1].get_right(), flow[1][0][2][1].get_left()).set_stroke(GREY, 2.0),  # 4 对1
            DashedLine(flow[1][0][2][1].get_right(), flow[1][2][0][1].get_left()).set_stroke(GREY, 2.0),  # 5
            CubicBezier(
                flow[1][2][2][0].get_bottom(),
                np.array([flow[1][2][2][0].get_bottom()[0], flow[2].get_left()[1] - 0.2, 0]),
                np.array([flow[1][2][2][0].get_bottom()[0] + 0.1, flow[2].get_left()[1] - 0.3, 0]),
                flow[2].get_left() + 0.3 * DOWN
            ).set_stroke(GREY, 2.0)
        )
        text_dim1 = MathTex("16*128*128").scale(0.5).next_to(flow[0], UP)
        text_dim2 = MathTex("16*128*128").scale(0.5).next_to(flow[2], UP)
        text_50_steps = Text("After 50 Steps", color=GREY).scale(0.6).next_to(text_dim2, UP)

        # ------------------decode-------------------
        self.model_vae_decoder.next_to(flow, RIGHT, buff=0.5)
        image_prompt = ImageMobject("assets/prompt.png").set(width=2.0).next_to(self.model_vae_decoder, DOWN, buff=0.5)
        arrow_flow_decode = Arrow(
            self.model_vae_decoder.get_left() + 0.8 * LEFT,
            self.model_vae_decoder.get_left(),
            color=GREY, stroke_width=4.0, buff=0.05, tip_length=0.2
        )
        arrow_decode_image = Arrow(
            self.model_vae_decoder.get_bottom(),
            image_prompt.get_top(),
            color=GREY, stroke_width=4.0, buff=0.05, tip_length=0.2
        )

        # ------------------time-------------------
        arrow_embedding = Arrow(
            flow.get_left() + 1.8 * DOWN + 0.5 * LEFT,
            flow.get_right() + 1.8 * DOWN + 0.5 * LEFT,
            color=GREY, stroke_width=2.0, tip_length=0.2
        )
        text_transformer = Text("Transformer", color=GREY).scale(0.5).next_to(arrow_embedding, DOWN)
        line_embedding = VGroup(
            Line(np.array([flow[1][0][1].get_bottom()[0] - 0.27, arrow_embedding.get_center()[1], 0]),
                 flow[1][0][1].get_bottom(), color=GREY, stroke_width=2.0),
            Line(np.array([flow[1][0][3].get_bottom()[0] - 0.27, arrow_embedding.get_center()[1], 0]),
                 flow[1][0][3].get_bottom(), color=GREY, stroke_width=2.0),
            Line(np.array([flow[1][2][1].get_bottom()[0] - 0.27, arrow_embedding.get_center()[1], 0]),
                 flow[1][2][1].get_bottom(), color=GREY, stroke_width=2.0)
        )
        text_step = Text("Step t").scale(0.4).next_to(arrow_embedding, LEFT, buff=0.9)
        line_step_arrow = Line(text_step.get_right() + 0.1 * RIGHT, arrow_embedding.get_left(), color=GREY,
                               stroke_width=2.0)

        # --------------------embedding-----------------
        embed1 = VGroup(
            RoundedRectangle(
                corner_radius=0.1, height=0.5, width=1.2, stroke_width=0.0
            ).set_fill(GREY, 0.4),
            MathTex(r"77*768").scale(0.5)
        )
        embed2 = VGroup(
            RoundedRectangle(
                corner_radius=0.1, height=0.5, width=1.6, stroke_width=0.0
            ).set_fill(GREY, 0.4),
            MathTex(r"77*1280").scale(0.5)
        ).next_to(embed1, RIGHT, buff=0.05)
        embed0 = VGroup(
            RoundedRectangle(
                corner_radius=0.1, height=0.5, width=1.3, stroke_width=0.0
            ).set_fill(GREY, 0.4)
        ).next_to(embed2, RIGHT, buff=0.05)
        embed3 = VGroup(
            RoundedRectangle(
                corner_radius=0.1, height=0.5, width=4.2, stroke_width=0.0
            ).set_fill(GREY, 0.4),
            MathTex(r"77*4096").scale(0.5)
        ).next_to(embed1, DOWN, buff=0.05).align_to(embed1, LEFT)
        VGroup(embed1[0], embed2[0], embed3[0]).set_submobject_colors_by_gradient(BLUE_D, GREEN)
        embedding = VGroup(embed0, embed1, embed2, embed3)
        (embedding.scale(0.7).rotate(PI / 2, about_point=embedding.get_center())
         .next_to(flow, LEFT, buff=0.7).shift(0.3 * UP))
        line_embedding_pooled = CubicBezier(
            embedding.get_bottom(),
            np.array([embedding.get_bottom()[0], arrow_embedding.get_center()[1] + 0.3, 0]),
            np.array([embedding.get_bottom()[0] + 0.3, arrow_embedding.get_center()[1], 0]),
            arrow_embedding.get_left()
        ).set_stroke(GREY, 2.0)
        line_embedding_input = CubicBezier(
            embedding.get_right(),
            embedding.get_right() + RIGHT,
            flow[1][0][0][1].get_left() + LEFT,
            flow[1][0][0][1].get_left()
        ).set_stroke(GREY, 2.0)

        # -------------------clip------------------
        clip1 = VGroup(
            SurroundingRectangle(
                Text("CLIP-L/14").scale(0.4), buff=0.1, corner_radius=0.1, stroke_width=0.0
            ).set_fill(GREY, 0.4),
            Text("CLIP-L/14").scale(0.4)
        )
        clip2 = VGroup(
            SurroundingRectangle(
                Text("CLIP-G/14").scale(0.4), buff=0.1, corner_radius=0.1, stroke_width=0.0
            ).set_fill(GREY, 0.4),
            Text("CLIP-G/14").scale(0.4)
        )
        clip3 = VGroup(
            SurroundingRectangle(
                Text("T5 XXL").scale(0.4), buff=0.1, corner_radius=0.1, stroke_width=0.0
            ).set_fill(GREY, 0.4),
            Text("T5 XXL").scale(0.4)
        )
        VGroup(clip1[0], clip2[0], clip3[0]).set_submobject_colors_by_gradient(BLUE_D, GREEN)
        clips = VGroup(clip1, clip2, clip3).arrange(DOWN, buff=0.3).next_to(embedding, DOWN, buff=1.0)
        self.prompt.set(width=2.4).next_to(clips, RIGHT, buff=1.0)
        lines_prompt_clip = VGroup(
            CubicBezier(
                self.prompt.get_left(),
                self.prompt.get_left() + 0.5 * LEFT,
                clip1.get_right() + 0.5 * RIGHT,
                clip1.get_right()
            ).set_stroke(GREY, 2.0),
            CubicBezier(
                self.prompt.get_left(),
                self.prompt.get_left() + 0.5 * LEFT,
                clip2.get_right() + 0.5 * RIGHT,
                clip2.get_right()
            ).set_stroke(GREY, 2.0),
            CubicBezier(
                self.prompt.get_left(),
                self.prompt.get_left() + 0.5 * LEFT,
                clip3.get_right() + 0.5 * RIGHT,
                clip3.get_right()
            ).set_stroke(GREY, 2.0)

        )

        # self.add(
        #     flow, text_dim1, text_dim2, lines_in_flow, arrow_embedding, line_embedding, embedding, clips,
        #     self.model_vae_decoder, image_prompt, arrow_flow_decode, arrow_decode_image, text_transformer,
        #     self.prompt, line_embedding_pooled, lines_prompt_clip, line_embedding_input, text_cross, line_mmdit_text
        #     , text_step, line_step_arrow
        # )
        self.play(FadeTransform(self.title_latent, self.title_sd3))
        self.play(Create(self.prompt))
        self.play(
            LaggedStartMap(FadeIn, clips, lag_ratio=0.5),
            LaggedStartMap(Create, lines_prompt_clip, lag_ratio=0.5)
        )
        self.play(LaggedStart(*[TransformFromCopy(clips[i], embedding[i + 1]) for i in range(3)], lag_ratio=0.3))
        self.play(FadeIn(embedding[0]))
        self.play(FadeIn(flow[0], shift=DOWN), Write(text_dim1))
        self.play(Create(flow[1][0][0]), Create(lines_in_flow[0]), Create(line_embedding_input))
        self.play(Write(text_step), Create(line_step_arrow), Create(line_embedding_pooled), Create(arrow_embedding))
        self.play(Create(lines_in_flow[1]), Create(lines_in_flow[4]), Create(line_embedding[0]), Create(flow[1][0][1]))
        self.play(Create(flow[1][0][2]), Create(flow[1][0][3]), Create(line_embedding[1]))
        self.play(Create(lines_in_flow[2]), Create(lines_in_flow[5]), Create(flow[1][1]))
        self.play(
            Create(flow[1][2][0]),
            Create(flow[1][2][1]),
            Create(lines_in_flow[3]),
            Create(flow[1][2][2]),
            Create(line_embedding[2]),
            Write(text_transformer)
        )
        self.play(Create(lines_in_flow[6]), FadeIn(flow[2], shift=DOWN), Write(text_dim2))
        self.play(Write(text_cross), LaggedStartMap(Create, line_mmdit_text))
        self.play(Write(text_50_steps))
        self.play(GrowArrow(arrow_flow_decode), FadeIn(self.model_vae_decoder, shift=DOWN))
        self.play(
            GrowArrow(arrow_decode_image),
            Rotate(self.gears_vae_decoder[0], axis=IN,
                   about_point=self.gears_vae_decoder[0].get_center()),
            FadeIn(image_prompt, shift=DOWN)
        )

        self.wait()


    def construct(self):
        self.camera.background_color = "#1C1C1C"
        self.sd3()


if __name__ == "__main__":
    SD3().render()
