from manim import *


class TracedPathExample(Scene):
    def construct(self):
        # circ = Circle(color=RED).shift(4 * LEFT)
        # dot = Dot(color=RED).move_to(circ.get_start())
        # rolling_circle = VGroup(circ, dot)
        # trace = TracedPath(circ.get_start)
        # rolling_circle.add_updater(lambda m: m.rotate(-PI / 2))
        # self.add(trace, rolling_circle)
        # self.play(rolling_circle.animate.shift(8 * RIGHT), run_time=4, rate_func=linear)

        radius_circle = 1

        circle_fix = Circle(radius=radius_circle,
                            color=GREY,
                            stroke_width=3)
        circle_mov = Circle(radius=radius_circle,
                            color=GREY,
                            stroke_width=3).rotate(PI)
        circle_mov.next_to(circle_fix, RIGHT, buff=0)
        dot = Dot(color=ORANGE).move_to(circle_mov.get_start())
        line = Line(start=circle_mov.get_center(),
                    end=dot.get_center(),
                    color=WHITE,
                    stroke_width=2)

        group_mov = VGroup(circle_mov, line, dot)
        trace = TracedPath(circle_mov.get_start)

        def update_group(group):
            theta = -0.1
            c, l, d = group
            c.rotate(theta, about_point=circle_fix.get_center())
            c.rotate(theta, about_point=c.get_center())
            d.move_to(c.get_start())
            l.put_start_and_end_on(c.get_center(), d.get_center())

        group_mov.add_updater(update_group)

        self.play(Create(circle_fix), Create(circle_mov))
        self.play(Create(line), Create(dot))
        self.wait()

        self.add(trace, group_mov)
        self.play(group_mov.animate.rotate(TAU),
                  rate_func=linear,
                  run_time=4)
        self.wait()

