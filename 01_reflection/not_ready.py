from manim import *
import numpy as np

COLOR_BACK = WHITE
COLOR_ENVELOPE = GREY

WIDTH_BACK = 3
WIDTH_ENVELOPE = 1.5

time_gap = 2
time_fadeout = 3
time_show_demo = 4
time_show_all = 7
time_draw_line = 4  # 画极坐标图像的时间

PLANE = NumberPlane(
    background_line_style={
        "stroke_color": TEAL,
        "stroke_width": 3
    }
)


def get_lines_for_reflection(num_points):
    lines = VGroup()
    actions = []
    radius_dot = 0.001
    radius_circle = 3
    dis_point = 3
    width = WIDTH_ENVELOPE if num_points > 100 else WIDTH_BACK
    run = time_show_all if num_points > 100 else time_show_demo
    circle = Circle(radius=radius_circle)
    for i in range(1, num_points):
        theta = i * 2 * PI / num_points
        phi = np.arctan(dis_point * np.sin(theta) / (radius_circle - dis_point * np.cos(theta)))
        theta_new = PI - 2 * phi + theta
        pos_out = np.array([np.cos(theta_new), np.sin(theta_new), 0]) * radius_circle
        p0 = Dot(radius=radius_dot).move_to(RIGHT * dis_point)
        p1 = Dot(radius=radius_dot).move_to(circle.point_at_angle(theta))
        p2 = Dot(radius=radius_dot).move_to(pos_out)
        line1 = Line(p0, p1, color=COLOR_ENVELOPE, stroke_width=width)
        line2 = Line(p1, p2, color=COLOR_ENVELOPE, stroke_width=width)
        actions.append(Create(VGroup(line1, line2), run_time=run))
        lines.add(line1)
        lines.add(line2)
    return actions, lines


def get_lines_for_multiply(num_points):
    dots = VGroup()
    lines = VGroup()
    radius_circle = 3
    width = WIDTH_ENVELOPE if num_points > 100 else WIDTH_BACK
    radius_dot = 0.01 if num_points > 100 else 0.05
    circle = Circle(radius=radius_circle)
    for i in range(num_points):
        dots.add(Dot(radius=radius_dot).move_to(
            circle.point_at_angle(PI / 2 + i * 2 * PI / num_points)))
    for i in range(num_points):
        lines.add(Line(dots[i], dots[(2 * i) % num_points],
                       color=COLOR_ENVELOPE,
                       stroke_width=width))
    return dots, lines


class Cardioid(Scene):
    def construct(self):
        self.play(FadeIn(PLANE), run_time=3)
        self.play(PLANE.animate.set_opacity(0.3))
        self.wait()
        self.by_rotate()
        self.by_reflection()
        self.by_multiply_two()

    def by_rotate(self):
        radius_circle = 1

        circle_fix = Circle(radius=radius_circle,
                            color=GREY,
                            stroke_width=WIDTH_BACK)
        circle_mov = Circle(radius=radius_circle,
                            color=GREY,
                            stroke_width=WIDTH_BACK).rotate(PI)
        circle_mov.next_to(circle_fix, RIGHT, buff=0)
        circle_mov.start_state = circle_mov.copy()
        dot = Dot(circle_mov.get_start(), color=ORANGE)
        line = Line(start=circle_mov.get_center(),
                    end=dot.get_center(),
                    color=COLOR_BACK,
                    stroke_width=WIDTH_ENVELOPE)
        path = VMobject(color=WHITE, stroke_width=WIDTH_BACK)
        path.append_vectorized_mobject(Line(dot.get_center(), dot.get_center()))
        group_mov = VGroup(circle_mov, line, dot, path)
        alpha = ValueTracker(0)

        def update_group(group):
            c, l, d, p = group
            c.become(c.start_state)
            c.rotate(TAU * alpha.get_value(), about_point=circle_fix.get_center())
            c.rotate(TAU * alpha.get_value(), about_point=c.get_center())
            d.move_to(c.get_start())
            p.add_line_to(d.get_center())
            p.make_smooth()
            l.put_start_and_end_on(c.get_center(), d.get_center())

        group_mov.add_updater(update_group)

        self.play(Create(circle_fix), Create(circle_mov))
        self.play(Create(line), Create(dot))
        self.wait(time_gap)

        self.add(circle_mov, group_mov)
        self.play(alpha.animate.set_value(1),
                  rate_func=linear,
                  run_time=time_show_all)
        self.wait(time_gap)

        self.play(FadeOut(line, dot),
                  FadeOut(circle_fix, shift=DOWN))
        self.play(FadeOut(circle_mov, shift=DOWN))
        self.wait(time_gap)

        self.play(FadeOut(path))
        self.wait(time_gap)

    def by_reflection(self):
        # 定义参数和元素
        radius_circle = 3
        num_demo = 8
        num_all = 128
        circle = Circle(radius=radius_circle, color=COLOR_BACK, stroke_width=WIDTH_BACK)
        dot = Dot(color=ORANGE).move_to(radius_circle * RIGHT)
        alpha = ValueTracker(0)
        path = VMobject(color=WHITE, stroke_width=WIDTH_BACK)

        def get_pos(theta):
            x = 2 * (1 + np.cos(theta)) * np.cos(theta) - 1
            y = 2 * (1 + np.cos(theta)) * np.sin(theta)
            return [x, y, 0]

        def update_path(p):
            p.append_vectorized_mobject(Line(p.points[-1], get_pos(alpha.get_value())))
            p.make_smooth()

        # 画圆和点
        self.play(Create(circle), Create(dot))
        self.wait(time_gap)

        # 画示例光线
        actions1, lines1 = get_lines_for_reflection(num_demo)
        self.play(*actions1)
        self.wait(time_gap)

        # 示例光线消失
        self.play(FadeOut(lines1))
        self.wait(time_gap)

        # 画全部光线
        actions2, lines2 = get_lines_for_reflection(num_all)
        self.play(*actions2)
        self.wait(time_gap)

        # 画极坐标图像
        path.append_vectorized_mobject(Line(get_pos(0.0), get_pos(0.001)))
        path.add_updater(update_path)
        self.add(path)
        self.play(alpha.animate.set_value(TAU), run_time=time_draw_line, rate_func=linear)
        self.wait(time_gap)

        self.play(FadeOut(circle, dot, lines2))
        self.wait(time_gap)

        self.play(FadeOut(path))
        self.wait(time_gap)

    def by_multiply_two(self):
        num_demo = 30
        num_all = 200

        dots1, lines1 = get_lines_for_multiply(num_demo)
        dots2, lines2 = get_lines_for_multiply(num_all)
        alpha = ValueTracker(0)
        path = VMobject(color=WHITE, stroke_width=WIDTH_BACK)

        def get_pos(theta):
            x = 2 * (1 + np.sin(theta)) * np.cos(theta)
            y = 2 * (1 + np.sin(theta)) * np.sin(theta) - 1
            return [x, y, 0]

        def update_path(p):
            p.append_vectorized_mobject(Line(p.points[-1], get_pos(alpha.get_value())))
            p.make_smooth()

        # 生成点
        self.play(Create(dots1, run_time=time_show_demo))
        self.wait(time_gap)

        # 画线
        self.play(Create(lines1, run_time=time_show_demo))
        self.wait(time_gap)

        # 线消失
        self.play(FadeOut(lines1))
        self.wait(time_gap)

        # 点增多
        self.play(ReplacementTransform(dots1, dots2))
        self.wait(time_gap)

        # 画线
        self.play(Create(lines2, run_time=time_show_all))
        self.wait(time_gap)

        # 画极坐标图像
        path.append_vectorized_mobject(Line(get_pos(0.0), get_pos(0.001)))
        path.add_updater(update_path)
        self.add(path)
        self.play(alpha.animate.set_value(TAU), run_time=time_draw_line, rate_func=linear)
        self.wait(time_gap)

        self.play(FadeOut(dots2, lines2))
        self.wait(time_gap)

        self.play(FadeOut(path))
        self.wait(time_gap)


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
