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


class Test(Scene):
    def construct(self):
        self.add(PLANE)
        self.by_rotate()
        # self.by_multiply_two()

    def by_rotate(self):
        radius_circle = 1

        circle_fix = Circle(radius=radius_circle, color=GREY, stroke_width=WIDTH_BACK)
        circle_mov = Circle(radius=radius_circle, color=GREY, stroke_width=WIDTH_BACK).rotate(PI)
        circle_mov.next_to(circle_fix, RIGHT, buff=0)
        circle_mov.start_state = circle_mov.copy()

        dot = Dot(circle_mov.point_from_proportion(0), color=ORANGE)
        line = Line(circle_mov.get_center(), dot.get_center(), color=COLOR_BACK, stroke_width=WIDTH_ENVELOPE)
        path = VMobject(color=WHITE, stroke_width=WIDTH_BACK)
        path.append_vectorized_mobject(Line(dot.get_center(), dot.get_center() + UP * 0.001))
        group_mov = VGroup(circle_mov, line, dot, path)
        alpha = ValueTracker(0)

        def update_group(group):
            c, l, d, p = group
            c.become(c.start_state)
            c.rotate(TAU * alpha.get_value(), about_point=circle_fix.get_center())
            c.rotate(TAU * alpha.get_value(), about_point=c.get_center())
            d.move_to(circle_mov.point_from_proportion(0))
            p.append_vectorized_mobject(Line(p.points[-1], dot.get_center()))
            p.make_smooth()
            l.put_start_and_end_on(circle_mov.get_center(), dot.get_center())

        group_mov.add_updater(update_group)

        self.play(Create(line), Create(circle_fix), Create(circle_mov), Create(dot))
        self.wait(time_gap)

        self.add(circle_mov, group_mov)
        self.play(alpha.animate.set_value(1),
                  rate_func=linear,
                  run_time=7
                  )
        self.wait(time_gap)

        self.play(FadeOut(line, circle_fix, circle_mov, dot))
        self.wait(time_gap)

        self.play(path.animate.scale(0.5).move_to(LEFT * 5 + UP * 2))
        self.wait(time_gap)
