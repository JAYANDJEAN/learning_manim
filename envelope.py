from manim import *
import numpy as np

COLOR_BACK = WHITE
COLOR_ENVELOPE = GREY

WIDTH_BACK = 3
WIDTH_ENVELOPE = 1.5

time_gap = 2
PLANE = NumberPlane(
    background_line_style={
        "stroke_color": TEAL,
        "stroke_width": 3,
        "stroke_opacity": 0.3
    }
)


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

        self.add(circle_show)
        self.play(Create(circle), Create(line))
        self.play(Rotating(dot, radians=PI,
                           about_point=ORIGIN,
                           run_time=time_show,
                           rate_func=there_and_back))
        self.wait(time_gap)

        self.add(circle_draw)
        self.play(MoveAlongPath(dot, circle), rate_func=linear, run_time=time_create)
        self.play(FadeOut(circle), FadeOut(line))
        self.wait(time_gap)
