from manim import *
import numpy as np

COLOR_BACK = WHITE
COLOR_ENVELOPE = GREY

WIDTH_BACK = 3
WIDTH_ENVELOPE = 1.5
PLANE = NumberPlane(
    background_line_style={
        "stroke_color": TEAL,
        "stroke_width": 3,
        "stroke_opacity": 0.3
    }
)


class MultiplyTwo(Scene):
    def construct(self):
        self.add(PLANE)
        time_create_dots = 2
        time_create_lines = 3
        time_gap = 2
        radius_circle = 3.5

        dots1 = self.get_dots(30, radius_circle, 0.05)
        dots2 = self.get_dots(400, radius_circle, 0.03)
        lines1 = self.get_lines(dots1, WIDTH_BACK)
        lines2 = self.get_lines(dots2, WIDTH_ENVELOPE)

        self.play(Create(dots1, run_time=time_create_dots))
        self.wait(time_gap)

        self.play(Create(lines1, run_time=time_create_lines))
        self.wait(time_gap)

        self.play(FadeOut(lines1))
        self.play(ReplacementTransform(dots1, dots2))
        self.wait(time_gap)
        self.play(Create(lines2, run_time=time_create_lines * 2))
        self.play(FadeOut(dots2))
        self.wait(time_gap)

    def get_dots(self, num_points, radius_circle, radius_dot):
        circle = Circle(radius=radius_circle)
        dots = VGroup()
        for i in range(num_points):
            dots.add(Dot(radius=radius_dot).move_to(
                circle.point_at_angle(PI / 2 + i * 2 * PI / num_points)))
        return dots

    def get_lines(self, dots, width):
        num_points = len(dots)
        lines = VGroup()
        for i in range(num_points):
            lines.add(Line(dots[i], dots[(2 * i) % num_points],
                           color=COLOR_ENVELOPE,
                           stroke_width=width))
        return lines


class CardioidByReflection(Scene):
    def construct(self):
        self.add(PLANE)
        radius_circle = 3
        time_show = 4
        time_create = 12

        circle = Circle(radius=radius_circle, color=COLOR_BACK, stroke_width=WIDTH_BACK)
        dot = Dot(color=ORANGE).move_to(radius_circle * RIGHT)

        self.play(Create(circle), Create(dot))
        self.wait()

        create_action_lines, lines = self.get_lines(radius_circle, 8, 0.3, WIDTH_BACK, time_show)
        self.play(*create_action_lines)
        self.wait(2)
        self.play(FadeOut(lines))
        self.wait(2)
        create_action_lines, lines = self.get_lines(radius_circle, 150, 1.0, WIDTH_ENVELOPE, time_create)
        self.play(*create_action_lines)
        self.wait(2)

    def get_lines(self, radius_circle, num_points, radio_d, width, rt):
        dots = VGroup()
        lines = VGroup()
        create_action_lines = []
        circle = Circle(radius=radius_circle)
        for i in range(num_points):
            theta = i * 2 * PI / num_points
            dots.add(Dot(radius=0.01).move_to(circle.point_at_angle(theta)))
            pos_out = np.array([np.cos(theta * 2) * radio_d + (1 - radio_d) * np.cos(theta),
                                np.sin(theta * 2) * radio_d + (1 - radio_d) * np.sin(theta),
                                0]) * radius_circle
            dots.add(Dot(radius=0.01).move_to(pos_out))

        for i in range(0, num_points * 2, 2):
            line_in = Line(dots[0], dots[i], color=COLOR_ENVELOPE, stroke_width=width)
            line_out = Line(dots[i], dots[i + 1], color=COLOR_ENVELOPE, stroke_width=width)
            create_action_lines.append(Create(VGroup(line_in, line_out), run_time=rt))
            lines.add(line_in, line_out)
        return create_action_lines, lines


class CircleLine(Scene):
    def __init__(self):
        super().__init__()
        self.index = 0

    def construct(self):
        self.add(PLANE)
        radius_circle = 1.5
        time_show = 4
        time_create = 12
        circle = Circle(radius=radius_circle, color=COLOR_BACK, stroke_width=WIDTH_BACK)
        dot = Dot(color=ORANGE).move_to(radius_circle * RIGHT)
        line = Line(radius_circle * 2 * LEFT, radius_circle * 2 * RIGHT,
                    color=COLOR_BACK, stroke_width=WIDTH_BACK)
        circle_list = VGroup()
        circle_show = Circle()
        circle_draw = VGroup()

        def circle_updater(mobject):
            new = Circle(radius=dot.get_center()[1], color=GREY, stroke_width=WIDTH_ENVELOPE)
            new.move_to(dot.get_center())
            mobject.become(new)

        def draw_updater(mobject):
            new = circle_show.copy()
            if self.index % 5 == 0:
                circle_list.add(new)
                mobject.become(circle_list)
            self.index += 1

        circle_show.add_updater(circle_updater)
        circle_draw.add_updater(draw_updater, index=10)

        self.wait()
        self.add(circle_show)
        self.play(Create(circle), Create(line))
        self.play(Rotating(dot, radians=PI,
                           about_point=ORIGIN,
                           run_time=time_show,
                           rate_func=there_and_back))
        self.wait()
        self.add(circle_draw)
        self.play(MoveAlongPath(dot, circle), rate_func=linear, run_time=time_create)
        self.play(FadeOut(circle), FadeOut(line))
        self.wait(3)
