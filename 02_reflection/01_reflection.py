import numpy as np
from manim import *
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


class Reflection(SameScene):
    def construct(self):
        def get_hyperbola(ha, hb):
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

        # 片头
        super().opening("Reflection I")

        ellipse = Ellipse(width=a * 2, height=b * 2, color=BLUE_B)
        dot_focus1 = Dot(color=ORANGE).move_to(RIGHT * c)
        dot_focus2 = Dot(color=ORANGE).move_to(LEFT * c)
        lines_from_focus = get_reflection_lines_from_focus(20)
        points_init = [(2.0, -get_y(2.0, a, b)),
                       (4.0, -get_y(4.0, a, b)),
                       (4.0, get_y(4.0, a, b)),
                       (4.95, get_y(4.95, a, b))]
        lines_reflection = [get_reflection_lines(x, y, 100)
                            for x, y in points_init]
        envelopes = []
        for x, y in points_init:
            new_a, new_b = get_new_ab(x, y)
            if y < 0:
                envelopes.append(get_hyperbola(new_a, new_b))
            else:
                envelopes.append(Ellipse(width=new_a * 2,
                                         height=new_b * 2,
                                         color=WHITE))

        time_play = 7
        time_draw = 3

        # 画椭圆和焦点
        self.play(Create(ellipse), Create(dot_focus1), Create(dot_focus2))
        self.wait(time_gap)

        # 画经过焦点的线
        text = super().caption("我们都知道从焦点发出的光线经椭圆反射，都会经过另一个焦点。")
        self.play(Create(lines_from_focus), run_time=time_play)
        self.wait(time_gap)
        self.play(FadeOut(text), FadeOut(lines_from_focus))

        # index:0，画椭圆内反射
        text = super().caption("如果光线并不经过焦点，那么光线会在椭圆内不断反射。比如像这样。")
        self.wait()
        self.play(Create(lines_reflection[0]), run_time=time_play)
        self.play(FadeOut(text))
        text = super().caption("这些光线形成的包络是双曲线，且双曲线的焦点与椭圆的焦点重合。")
        self.play(Create(envelopes[0]), run_time=time_draw)
        self.wait(time_gap)
        self.play(FadeOut(text), FadeOut(lines_reflection[0]))
        self.wait(time_gap)
        self.play(FadeOut(envelopes[0]))
        self.wait(time_gap)

        # index:1，
        text = super().caption("我们可以再举个例子。")
        self.play(Create(lines_reflection[1]), run_time=time_play)
        self.play(Create(envelopes[1]), run_time=time_draw)
        self.play(FadeOut(text), FadeOut(lines_reflection[1]))
        self.wait(time_gap)
        self.play(FadeOut(envelopes[1]))
        self.wait(time_gap)

        # index:2，
        text = super().caption("光线在椭圆内的反射也可以形成另一个椭圆。比如像这样。")
        self.wait()
        self.play(Create(lines_reflection[2]), run_time=time_play)
        self.wait(time_gap)
        self.play(Create(envelopes[2]), run_time=time_draw)
        self.wait(time_gap)
        self.play(FadeOut(text), FadeOut(lines_reflection[2]))
        self.wait(time_gap)
        self.play(FadeOut(envelopes[2]))
        self.wait(time_gap)

        # index:3，
        text = super().caption("同样我们可以再举个例子。")
        self.play(Create(lines_reflection[3]), run_time=time_play)
        self.play(Create(envelopes[3]), run_time=time_draw)
        self.play(FadeOut(text), FadeOut(lines_reflection[3]))
        self.wait(time_gap)
        self.play(FadeOut(envelopes[3]))
        self.wait(time_gap)

        #
        text = super().caption("那怎么证明呢？我还在写。")
        self.wait(time_gap)
        self.play(FadeOut(text))

        # 清理最后的

        self.play(FadeOut(dot_focus2),
                  FadeOut(dot_focus1),
                  FadeOut(ellipse, shift=DOWN))
        self.wait(time_gap)
