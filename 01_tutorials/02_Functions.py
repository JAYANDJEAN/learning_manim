from manim import *


class PlotExample(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1]).add_coordinates()
        axes = Axes()
        axes.to_edge(UR)
        axis_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        graph = axes.plot(lambda x: x ** 0.5, x_range=[0, 4], color=YELLOW, use_smoothing=True)
        graphing_stuff = VGroup(axes, graph, axis_labels)

        self.play(FadeIn(plane), run_time=3)
        self.play(plane.animate.set_opacity(0.3))
        self.wait()
        self.play(DrawBorderThenFill(axes), Write(axis_labels), run_time=2)
        self.wait()
        self.play(Create(graph), run_time=2)
        self.play(graphing_stuff.animate.shift(DOWN * 4), run_time=3)
        self.wait()
        self.play(axes.animate.shift(LEFT * 3), run_time=3)
        self.wait()


class HorizontalLineExample(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1]).add_coordinates()
        axe = Axes().add_coordinates()
        axe.shift(RIGHT * 3)

        def func(x):
            return 0.1 * (x - 5) * x * (x + 5)

        graph = axe.plot(func, x_range=[-6, 6], color=GREEN_B)
        label = MathTex("f(x)=0.1x(x-5)(x+5)").next_to(axe, UP, buff=0.2)
        area = axe.get_area(graph=graph, x_range=[-5, 5], color=[BLUE, YELLOW])

        horizontal_line = axe.get_horizontal_line(
            axe.c2p(1, func(1), 0), color=BLUE, stroke_width=5)

        self.play(FadeIn(plane), run_time=3)
        self.play(plane.animate.set_opacity(0.2))
        self.wait()
        self.play(DrawBorderThenFill(axe), run_time=2)
        self.wait()
        self.play(Create(graph), Write(label), run_time=2)
        self.wait()
        self.play(FadeIn(area), run_time=2)
        self.wait()
        self.play(Create(horizontal_line), run_time=2)
        self.wait()


class GraphExample(Scene):
    def construct(self):
        e = ValueTracker(0.01)
        plane = PolarPlane(radius_max=3).add_coordinates()
        plane.shift(LEFT * 3)
        graph1 = always_redraw(
            lambda: ParametricFunction(
                lambda t: plane.polar_to_point(2 * np.sin(3 * t), t),
                t_range=[0, e.get_value()],
                color=GREEN
            )
        )
        dot1 = always_redraw(
            lambda: Dot(fill_color=RED,
                        fill_opacity=0.8).scale(0.5).move_to(graph1.get_end())
        )

        axes = Axes(x_range=[0, 4, 1], x_length=3,
                    y_range=[-3, 3, 1], y_length=3) \
            .shift(RIGHT * 3).add_coordinates()
        graph2 = always_redraw(
            lambda: axes.plot(
                lambda x: 2 * np.sin(3 * x), x_range=[0, e.get_value()], color=GREEN
            )
        )
        dot2 = always_redraw(
            lambda: Dot(fill_color=RED,
                        fill_opacity=0.8).scale(0.5).move_to(graph2.get_end())
        )

        title = MathTex("f(\\theta) = 2sin(3\\theta)", color=GREEN).next_to(axes, UP, buff=0.2)

        self.play(LaggedStart(
            Write(plane), Create(axes), Write(title),
            run_time=3, lag_ratio=0.5)
        )
        self.add(graph1, graph2, dot1, dot2)
        self.play(e.animate.set_value(PI), run_time=10, rate_func=linear)
        self.wait()


class RiemannExample(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1]).add_coordinates()
        graph = plane.plot(lambda x: x ** 2, x_range=[-4, 4], color=GREEN)
        area = plane.get_riemann_rectangles(graph=graph, x_range=[-2, 2], dx=0.1)
        v_lines = plane.get_vertical_lines_to_graph(graph=graph, x_range=[-2, 2], num_lines=12)

        self.play(FadeIn(plane), run_time=3)
        self.play(plane.animate.set_opacity(0.3))
        self.wait()
        self.play(Create(graph), run_time=2)
        self.wait()
        self.play(Create(area), run_time=2)
        self.wait()
        self.play(FadeOut(area))
        self.wait()
        self.play(Create(v_lines), run_time=2)
        self.wait()


class ComplexPlaneExample(Scene):
    def construct(self):
        plane = ComplexPlane(axis_config={"include_tip": True, "numbers_to_exclude": [0]}).add_coordinates()

        labels = plane.get_axis_labels(x_label="Real", y_label="Imaginary")

        quest = MathTex("Plot \\quad 2-3i").add_background_rectangle().to_edge(UL)
        dot = Dot()
        vect1 = plane.get_vector((2, 0), stroke_color=YELLOW)
        vect2 = Line(start=plane.c2p(2, 0),
                     end=plane.c2p(2, -3), stroke_color=YELLOW).add_tip()

        self.play(DrawBorderThenFill(plane), Write(labels))
        self.wait()
        self.play(FadeIn(quest))
        self.play(GrowArrow(vect1), dot.animate.move_to(plane.c2p(2, 0)), rate_func=linear, run_time=2)
        self.wait()
        self.play(GrowFromPoint((vect2), point=vect2.get_start()),
                  dot.animate.move_to(plane.c2p(2, -3)), run_time=2, rate_func=linear)
        self.wait()
