from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService
from utils import *


def get_lines_for_reflection(num_points, long, short):
    lines = VGroup()
    actions = []
    width = 1.5 if num_points > 100 else 3
    run = 7 if num_points > 100 else 3

    for i in range(1, num_points):
        theta = i * 2 * PI / num_points
        x1 = Circle(radius=long).point_at_angle(theta)[0]
        for y1 in [get_y(x1, long, short), -get_y(x1, long, short)]:
            x2, y2 = get_reflection_line(long, 0, x1, y1, long, short)
            line1 = Line(np.array([long, 0, 0]),
                         np.array([x1, y1, 0]),
                         stroke_width=width,
                         color=GREY)
            line2 = Line(np.array([x1, y1, 0]),
                         np.array([x2, y2, 0]),
                         stroke_width=width,
                         color=GREY)
            actions.append(Create(VGroup(line1, line2), run_time=run))
            lines.add(line1)
            lines.add(line2)
    return actions, lines


class Point(VoiceoverScene):
    def __init__(self):
        super().__init__()
        self.plane = NumberPlane(
            background_line_style={
                "stroke_color": "#C2C2C2",
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        )
        self.camera.background_color = "#1C1C1C"
        self.set_speech_service(
            AzureService(voice="zh-CN-YunhaoNeural")
        )

    def construct(self):
        self.add(self.plane)
        title = Text("Reflection II").scale(3)
        logo = MathTex(r"\mathbb{JAYANDJEAN}", fill_color="#ece6e2").next_to(title, DOWN, buff=0.5).scale(2)
        self.play(Write(title))
        self.play(Write(logo))
        self.play(FadeOut(title))
        self.play(logo.animate.scale(0.4).move_to(RIGHT * 5.4 + UP * 3.2))
        self.wait()

        num_demo = 8
        num_all = 128
        cardioid = self.plane.plot_parametric_curve(
            lambda t: np.array(
                [2 * (1 + np.cos(t)) * np.cos(t) - 1,
                 2 * (1 + np.cos(t)) * np.sin(t),
                 0]
            ),
            t_range=[0, TAU],
            color=WHITE,
        )
        circle = Circle(radius=r, color=BLUE_B, stroke_width=3)
        dot1 = Dot(color=ORANGE).move_to(r * RIGHT)
        dot2 = Dot(color=ORANGE).move_to(a * RIGHT)
        actions1, lines1 = get_lines_for_reflection(num_demo, r, r)
        actions2, lines2 = get_lines_for_reflection(num_all, r, r)
        actions3, lines3 = get_lines_for_reflection(num_all, a, b)
        ellipse = Ellipse(width=a * 2, height=b * 2, color=BLUE_B)

        with self.voiceover(
                """
                我们先从简单的例子出发，可视化光线在圆里的反射。
                """
        ):
            self.play(Create(circle), Create(dot1))

        with self.voiceover(
                """
                光线经圆的内壁反射，比如像这样。
                """
        ):
            self.play(*actions1)
        self.play(FadeOut(lines1))

        with self.voiceover(
                """
                增加光线数量，以模拟真实场景。
                """
        ):
            self.play(*actions2)

        with self.voiceover(
                """
                光线形成的包络是心脏线。
                """
        ):
            self.play(Create(cardioid), run_time=4)
        self.play(FadeOut(circle, dot1, lines2))
        self.play(FadeOut(cardioid))

        with self.voiceover(
                """
                现在可视化光线在椭圆内的反射。这个形成的包络是什么曲线呢？
                """
        ):
            self.play(Create(ellipse), Create(dot2))
            self.play(*actions3)
        self.wait()
        self.play(FadeOut(lines3))
        self.play(FadeOut(ellipse, shift=DOWN), FadeOut(dot2, shift=DOWN))
        self.wait()
