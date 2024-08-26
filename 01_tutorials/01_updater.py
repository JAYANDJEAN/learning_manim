from manim import *
import numpy as np
import random

'''
了解 always_redraw 的用法，与 add_updater 的差异
'''


class Scene1(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1]).add_coordinates()
        box = Rectangle(stroke_color=GREEN_C,
                        stroke_opacity=0.7,
                        fill_color=RED_B,
                        fill_opacity=0.5,
                        height=1,
                        width=1)

        dot = always_redraw(lambda: Dot().move_to(box.get_center()))

        self.play(FadeIn(plane), run_time=2)
        self.wait()
        self.add(box, dot)
        self.play(box.animate.shift(RIGHT * 2), run_time=4)
        self.wait()
        self.play(box.animate.shift(UP * 3), run_time=4)
        self.wait()


class Scene2(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1]).add_coordinates()

        axes = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=6, y_length=6)
        axes.to_edge(LEFT, buff=0.5)

        circle = Circle(stroke_width=6, stroke_color=YELLOW, fill_color=RED_C, fill_opacity=0.8)
        circle.set_width(2).to_edge(DR, buff=0)

        triangle = Triangle(stroke_color=ORANGE, stroke_width=10,
                            fill_color=GREY).set_height(2).shift(DOWN * 3 + RIGHT * 3)

        # 了解一般动画效果
        self.play(FadeIn(plane), run_time=6)
        self.wait()
        self.play(Write(axes))
        self.wait()
        self.play(plane.animate.set_opacity(0.4))
        self.wait()
        self.play(DrawBorderThenFill(circle))
        self.wait()
        self.play(circle.animate.set_width(1))
        self.wait()
        self.play(Transform(circle, triangle), run_time=3)
        self.wait()


class Scene3(Scene):
    def construct(self):
        rectangle = RoundedRectangle(stroke_width=8, stroke_color=WHITE,
                                     fill_color=BLUE_B, width=4.5, height=2).shift(UP * 3 + LEFT * 4)

        mathtext = MathTex("\\frac{3}{4} = 0.75").set_color_by_gradient(GREEN, PINK).set_height(1.5)
        mathtext.move_to(rectangle.get_center())

        # add_updater 的用法
        mathtext.add_updater(lambda x: x.move_to(rectangle.get_center()))

        self.play(FadeIn(rectangle))
        self.wait()
        self.play(Write(mathtext), run_time=2)
        self.wait()

        self.play(rectangle.animate.shift(RIGHT * 1.5 + DOWN * 5), run_time=6)
        self.wait()
        mathtext.clear_updaters()
        self.play(rectangle.animate.shift(LEFT * 2 + UP * 1), run_time=6)
        self.wait()


class Scene4(Scene):
    def construct(self):
        r = ValueTracker(0.5)  # Tracks the value of the radius

        circle = always_redraw(lambda: Circle(radius=r.get_value(),
                                              stroke_color=YELLOW,
                                              stroke_width=5)
                               )

        line_radius = always_redraw(lambda: Line(start=circle.get_center(),
                                                 end=circle.get_bottom(),
                                                 stroke_color=RED_B,
                                                 stroke_width=10)
                                    )

        line_circumference = always_redraw(lambda: Line(stroke_color=YELLOW,
                                                        stroke_width=5
                                                        )
                                           .set_length(2 * r.get_value() * PI)
                                           .next_to(circle, DOWN, buff=0.2)
                                           )

        triangle = always_redraw(lambda: Polygon(circle.get_top(),
                                                 circle.get_left(),
                                                 circle.get_right(),
                                                 fill_color=GREEN_C)
                                 )

        self.play(LaggedStart(Create(circle),
                              DrawBorderThenFill(line_radius),
                              DrawBorderThenFill(triangle),
                              run_time=4, lag_ratio=0.75
                              )
                  )
        self.play(ReplacementTransform(circle.copy(), line_circumference), run_time=2)
        self.play(r.animate.set_value(2), run_time=5)


class Scene5(Scene):
    def construct(self):
        # 画极坐标方程
        e = ValueTracker(0)
        plane = PolarPlane().add_coordinates()
        graph = always_redraw(lambda: ParametricFunction(
            lambda t: plane.polar_to_point(2 * (1 + np.sin(t)), t),
            t_range=[0, e.get_value()], color=WHITE, stroke_width=3))
        self.add(graph)
        self.play(Create(plane), run_time=5)
        self.play(e.animate.set_value(TAU), run_time=5, rate_func=linear)
        self.wait()


class Scene6(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes().add_coordinates()
        end = ValueTracker(-4.9)

        graph = always_redraw(
            lambda: ParametricFunction(
                lambda t: np.array([4 * np.cos(t), 4 * np.sin(t), 0.5 * t]),
                color=BLUE, t_range=[-5, end.get_value()])
        )

        line = always_redraw(
            lambda: Line(start=ORIGIN, end=graph.get_end(), color=BLUE).add_tip()
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=-30 * DEGREES)
        self.add(axes, graph, line)
        self.play(end.animate.set_value(5), run_time=3)
        self.wait()
