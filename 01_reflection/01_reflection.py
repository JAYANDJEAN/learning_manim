from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

from utils import *

X_S = 0
Y_S = b


def get_new_ab(x1, y1):
    s, t = (Y_S - y1) / Y_S / x1, 1 / Y_S
    denominator = np.square(s) + np.square(t)
    ha = np.sqrt((1 + np.square(t * c)) / denominator)
    hb = np.sqrt(np.abs((1 - np.square(s * c))) / denominator)
    return ha, hb


def get_reflection_lines(x1, y1, num):
    x0, y0 = X_S, Y_S
    lines = VGroup()
    lines.add(Line(np.array([x0, y0, 0]),
                   np.array([x1, y1, 0]),
                   stroke_width=1.5))
    for i in range(num):
        x2, y2 = get_reflection_line(x0, y0, x1, y1, a, b)
        lines.add(Line(np.array([x1, y1, 0]),
                       np.array([x2, y2, 0]),
                       stroke_width=1.5))
        x0, y0, x1, y1 = x1, y1, x2, y2
    lines.set_color_by_gradient(BLUE, YELLOW, RED)
    return lines


def get_reflection_lines_from_focus(num):
    lines = VGroup()
    x0, y0 = c, 0
    for x1 in np.linspace(-c + 0.1, c - 0.1, num):
        y1 = get_y(x1, a, b)
        x2, y2 = get_reflection_line(x0, y0, x1, y1, a, b)
        lines.add(Line(np.array([x0, y0, 0]),
                       np.array([x1, y1, 0]),
                       stroke_width=1.5))
        lines.add(Line(np.array([x1, y1, 0]),
                       np.array([x2, y2, 0]),
                       stroke_width=1.5))
    lines.set_color_by_gradient(BLUE, YELLOW, RED)
    return lines


class Reflection(VoiceoverScene):
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
        title = Text("Reflection I").scale(3)
        logo = MathTex(r"\mathbb{JAYANDJEAN}", fill_color="#ece6e2").next_to(title, DOWN, buff=0.5).scale(2)
        self.play(Write(title))
        self.play(Write(logo))
        self.play(FadeOut(title))
        self.play(logo.animate.scale(0.4).move_to(RIGHT * 5.4 + UP * 3.2))
        self.wait()

        ellipse = Ellipse(width=a * 2, height=b * 2, color=BLUE_B)
        dot_focus1 = Dot(color=ORANGE).move_to(RIGHT * c)
        dot_focus2 = Dot(color=ORANGE).move_to(LEFT * c)
        lines_from_focus = get_reflection_lines_from_focus(20)
        points_init = [(2.0, -get_y(2.0, a, b)),
                       (4.0, -get_y(4.0, a, b)),
                       (4.0, get_y(4.0, a, b)),
                       (4.95, get_y(4.95, a, b))]
        lines_reflection = [get_reflection_lines(x, y, 100) for x, y in points_init]
        envelopes = []
        for x, y in points_init:
            new_a, new_b = get_new_ab(x, y)
            if y < 0:
                envelopes.append(self.get_hyperbola(new_a, new_b))
            else:
                envelopes.append(Ellipse(width=new_a * 2, height=new_b * 2, color=WHITE))

        with self.voiceover(
                """
                我们都知道从焦点发出的光线经椭圆反射，都会经过另一个焦点。
                """
        ):
            self.play(Create(ellipse), Create(dot_focus1), Create(dot_focus2))
            self.wait()
            self.play(Create(lines_from_focus), run_time=3)
            self.play(FadeOut(lines_from_focus))

        with self.voiceover(
                """
                如果光线并不经过焦点，那么光线会在椭圆内不断反射。比如像这样。
                """
        ):
            self.wait()
            self.play(Create(lines_reflection[0]), run_time=4)

        with self.voiceover(
                """
                这些光线形成的包络是双曲线，且双曲线的焦点与椭圆的焦点重合。
                """
        ):
            self.play(Create(envelopes[0]), run_time=2)
        self.play(FadeOut(lines_reflection[0]))
        self.play(FadeOut(envelopes[0]))

        with self.voiceover(
                """
                我们可以再举个例子。
                """
        ):
            self.play(Create(lines_reflection[1]), run_time=3)
            self.play(Create(envelopes[1]), run_time=2)
            self.play(FadeOut(lines_reflection[1]))
            self.play(FadeOut(envelopes[1]))

        with self.voiceover(
                """
                光线在椭圆内的反射也可以形成另一个椭圆。比如像这样。
                """
        ):
            self.play(Create(lines_reflection[2]), run_time=3)
            self.play(Create(envelopes[2]), run_time=2)
            self.play(FadeOut(lines_reflection[2]))
            self.play(FadeOut(envelopes[2]))

        with self.voiceover(
                """
                同样我们可以再举个例子。
                """
        ):
            self.play(Create(lines_reflection[3]), run_time=3)
            self.play(Create(envelopes[3]), run_time=2)
            self.play(FadeOut(lines_reflection[3]))
            self.play(FadeOut(envelopes[3]))

        self.play(FadeOut(dot_focus2), FadeOut(dot_focus1), FadeOut(ellipse, shift=DOWN))
        self.wait()

    def get_hyperbola(self, ha, hb):
        graph = VGroup()
        hyperbola1 = self.plane.plot_parametric_curve(
            lambda t: np.array(
                [ha * np.cosh(t),
                 hb * np.sinh(t),
                 0]
            ),
            t_range=[-2, 2],
        )
        graph.add(hyperbola1)
        hyperbola2 = self.plane.plot_parametric_curve(
            lambda t: np.array(
                [-ha * np.cosh(t),
                 hb * np.sinh(t),
                 0]
            ),
            t_range=[-2, 2],
        )
        graph.add(hyperbola2)
        return graph
