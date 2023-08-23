from manim import *


class TextItalicAndBoldExample(Scene):
    def construct(self):
        number_plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.3
            }
        )
        self.add(number_plane)

        circle = Circle(radius=3.5)
        circle_group = Group()
        for i in range(40):
            d = Dot().move_to(circle.point_at_angle(PI / 2 + i * 2 * PI / 40))
            circle_group.add(d)
            self.add(d)
            self.wait(0.1)

        circle_group2 = Group()
        for i in range(50):
            d = Dot(radius=0.03).move_to(circle.point_at_angle(PI / 2 + i * 2 * PI / 50))
            circle_group2.add(d)

        self.play(ReplacementTransform(circle_group, circle_group2))
        self.wait(2.0)

    def add_dot_and_lines(self, num_points, radius_circle):
        circle = Circle(radius=radius_circle)
        circle_group = Group()
        for i in range(num_points):
            d = Dot().move_to(circle.point_at_angle(PI / 2 + i * 2 * PI / num_points))
            circle_group.add(d)
            self.add(d)
            self.wait(0.1)
        for i in range(num_points):
            l = Line(circle_group[i], circle_group[(2 * i) % num_points])
            self.add(l)
            self.wait(0.1)
        self.wait(1.0)
