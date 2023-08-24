from manim import *


class Test(Scene):
    def construct(self):
        number_plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 3,
                "stroke_opacity": 0.3
            }
        )
        self.add(number_plane)
        time_create_dots = 2
        time_create_lines = 3
        time_gap = 2
        radius_circle = 3.5

        dots1 = self.get_dots(30, radius_circle, 0.05)
        dots2 = self.get_dots(300, radius_circle, 0.03)
        dots3 = self.get_dots(1000, radius_circle, 0.02)
        lines1 = self.get_lines(dots1)
        lines2 = self.get_lines(dots2)
        lines3 = self.get_lines(dots3)

        self.play(Create(dots1, run_time=time_create_dots))
        self.wait(time_gap)

        self.play(Create(lines1, run_time=time_create_lines))
        self.wait(time_gap)

        self.play(FadeOut(lines1))
        self.play(ReplacementTransform(dots1, dots2))
        self.play(Create(lines2, run_time=time_create_lines))
        self.wait(time_gap)

        self.play(FadeOut(lines2))
        self.play(ReplacementTransform(dots2, dots3))
        self.play(Create(lines3, run_time=time_create_lines))
        self.wait(time_gap)

    def get_dots(self, num_points, radius_circle, radius_dot):
        circle = Circle(radius=radius_circle)
        dots = VGroup()
        for i in range(num_points):
            dots.add(Dot(radius=radius_dot).move_to(
                circle.point_at_angle(PI / 2 + i * 2 * PI / num_points)))
        return dots

    def get_lines(self, dots):
        num_points = len(dots)
        lines = VGroup()
        for i in range(num_points):
            lines.add(Line(dots[i], dots[(2 * i) % num_points],
                           color='#FFFFF0',
                           stroke_width=1.5,
                           stroke_opacity=0.5))
        return lines


class Cir_line(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        radius_circle = 1.5

        circle = Circle(radius=radius_circle, color=BLUE, stroke_width=1.5)
        dot = Dot(color=RED).move_to(radius_circle * RIGHT)
        line = Line(radius_circle * 2 * LEFT, radius_circle * 2 * RIGHT, color=BLUE_B, stroke_width=1.5)

        draw = VGroup()

        def circle_updater(mobject):
            c = Circle(radius=dot.get_center()[1], color=PINK, stroke_width=1)
            c.move_to(dot.get_center())
            mobject.become(c)

        def draw_updater(mobject):
            c = circle_f.copy()
            mobject.add(c)

        circle_f = Circle().add_updater(circle_updater)
        draw.add_updater(draw_updater)

        self.add(dot, circle_f)
        self.play(Create(circle), Create(line))
        self.play(Rotating(dot, radians=TAU, about_point=ORIGIN, run_time=4, rate_func=there_and_back))
        self.wait()
        self.add(draw)
        print(len(draw))
        self.play(MoveAlongPath(dot, circle), rate_func=linear, run_time=12)
        self.wait(3)


class NextToUpdater(Scene):
    def construct(self):
        def dot_position(mobject):
            mobject.set_value(dot.get_center()[0])
            mobject.next_to(dot)

        dot = Dot(RIGHT * 3)
        label = DecimalNumber()
        label.add_updater(dot_position)
        self.add(dot, label)

        self.play(Rotating(dot, about_point=ORIGIN, angle=TAU, run_time=TAU, rate_func=linear))
