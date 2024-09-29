from utils import *


class SD(Diffusion):
    def __init__(self):
        super().__init__()

    def sd3(self):
        self.prompt.scale(0.6).move_to(5.5 * LEFT + 2 * UP)
        clip1 = VGroup(
            SurroundingRectangle(
                Text("CLIP-L/14").scale(0.5), buff=0.1, corner_radius=0.1, stroke_width=0.0
            ).set_fill(GREY, 0.4),
            Text("CLIP-L/14").scale(0.5)
        )
        clip2 = VGroup(
            SurroundingRectangle(
                Text("CLIP-G/14").scale(0.5), buff=0.1, corner_radius=0.1, stroke_width=0.0
            ).set_fill(GREY, 0.4),
            Text("CLIP-G/14").scale(0.5)
        )
        clip3 = VGroup(
            SurroundingRectangle(
                Text("T5 XXL").scale(0.5), buff=0.1, corner_radius=0.1, stroke_width=0.0
            ).set_fill(GREY, 0.4),
            Text("T5 XXL").scale(0.5)
        )
        VGroup(clip1[0], clip2[0], clip3[0]).set_submobject_colors_by_gradient(BLUE_D, GREEN)
        clips = VGroup(clip1, clip2, clip3).arrange(DOWN, buff=0.4).to_edge(DOWN).shift(4 * LEFT)

        embed1 = VGroup(
            RoundedRectangle(
                corner_radius=0.1, height=0.5, width=1.2, stroke_width=0.0
            ).set_fill(GREY, 0.4),
            Text(r"77*768").scale(0.5)
        )
        embed2 = VGroup(
            RoundedRectangle(
                corner_radius=0.1, height=0.5, width=1.6, stroke_width=0.0
            ).set_fill(GREY, 0.4),
            Text(r"77*1280").scale(0.5)
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
            Text(r"77*4096").scale(0.5)
        ).next_to(embed1, DOWN, buff=0.05).align_to(embed1, LEFT)
        VGroup(embed1[0], embed2[0], embed3[0]).set_submobject_colors_by_gradient(BLUE_D, GREEN)
        embedding = VGroup(embed0, embed1, embed2, embed3).next_to(clips, RIGHT, buff=1.0)

        lines_out_image = VGroup(
            *[
                CubicBezier(
                    self.prompt.get_bottom(),
                    np.array([self.prompt.get_bottom()[0], c.get_left()[1], 0]),
                    np.array([self.prompt.get_bottom()[0], c.get_left()[1], 0]),
                    c.get_left(),
                    stroke_width=2.0
                ) for c in clips]
        )
        noise = SVGMobject("assets/prism1.svg").scale(1.5).move_to(3 * LEFT + UP)

        data_input = VGroup(
            VGroup(
                RoundedRectangle(
                    corner_radius=0.1, height=1.2, width=1.3, stroke_width=0.0
                ).set_fill("#FD8244", 0.4),
                Text(r"4096*1536").scale(0.4)
            ),
            VGroup(
                RoundedRectangle(
                    corner_radius=0.1, height=0.55, width=1.3, stroke_width=0.0
                ).set_fill("#FD8244", 0.4),
                Text(r"154*1536").scale(0.4)
            )
        ).arrange(DOWN, buff=0.4).next_to(noise, RIGHT)

        self.add(self.prompt, clips, lines_out_image, embedding, noise, data_input)
        # self.play(LaggedStartMap(FadeIn, clips, lag_ratio=0.5, shift=DOWN))
        # self.wait()

    def construct(self):
        self.camera.background_color = "#1C1C1C"
        self.sd3()


if __name__ == "__main__":
    SD().render()
