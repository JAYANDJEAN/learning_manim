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


def get_lines_1(radius_circle, num_points, dis_point, width, rt):
    lines = VGroup()
    actions = []
    radius_dot = 0.001
    circle = Circle(radius=radius_circle)
    for i in range(num_points):
        theta = i * 2 * PI / num_points
        phi = np.arctan(dis_point * np.sin(theta) / (radius_circle - dis_point * np.cos(theta)))
        theta_new = PI - 2 * phi + theta
        pos_out = np.array([np.cos(theta_new), np.sin(theta_new), 0]) * radius_circle
        p0 = Dot(radius=radius_dot).move_to(RIGHT * dis_point)
        p1 = Dot(radius=radius_dot).move_to(circle.point_at_angle(theta))
        p2 = Dot(radius=radius_dot).move_to(pos_out)
        line1 = Line(p0, p1, color=COLOR_ENVELOPE, stroke_width=width)
        line2 = Line(p1, p2, color=COLOR_ENVELOPE, stroke_width=width)
        actions.append(Create(VGroup(line1, line2), run_time=rt))
        lines.add(line1, line2)
    return actions, lines


def get_lines_2(num_points, radius_circle, radius_dot, width):
    dots = VGroup()
    lines = VGroup()
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
        self.add(PLANE)

        self.by_rotate()
        self.by_reflection()
        self.by_multiply_two()

    def by_reflection(self):
        radius_circle = 3
        time_show = 4
        time_create = 10
        time_draw_line = 4  # 画极坐标图像的时间
        num_demo = 8
        num_all = 128
        dis_point = 4

        circle = Circle(radius=radius_circle, color=COLOR_BACK, stroke_width=WIDTH_BACK)
        dot = Dot(color=ORANGE).move_to(radius_circle * RIGHT)

        # 画圆和点
        self.play(Create(circle), Create(dot))
        self.wait(time_gap)

        # 画实例光线
        create_action_lines, lines = \
            get_lines_1(radius_circle, num_demo, radius_circle, WIDTH_BACK, time_show)
        self.play(*create_action_lines)
        self.wait(time_gap)

        # 示例光线消失，画全部光线
        self.play(FadeOut(lines))
        create_action_lines, lines = \
            get_lines_1(radius_circle, num_all, radius_circle, WIDTH_ENVELOPE, time_create)
        self.play(*create_action_lines)
        self.wait(time_gap)

        # 画极坐标图像
        e = ValueTracker(0.01)
        plane = PolarPlane().add_coordinates().move_to(LEFT)
        graph = always_redraw(lambda: ParametricFunction(
            lambda t: plane.polar_to_point(2 * (1 + np.cos(t)), t),
            t_range=[0, e.get_value()], color=COLOR_BACK, stroke_width=WIDTH_BACK))
        self.add(graph)
        self.play(e.animate.set_value(2 * PI), run_time=time_draw_line, rate_func=linear)
        self.wait(time_gap)

        # # 全部光线和函数图像消失，移动点，画示例光线
        # self.play(FadeOut(graph, lines))
        # create_action_lines, lines = \
        #     self.get_lines_1(radius_circle, num_demo, dis_point, WIDTH_BACK, time_show)
        # dot.generate_target()
        # dot.target.shift((dis_point - radius_circle) * RIGHT)
        # self.play(MoveToTarget(dot))
        # self.play(*create_action_lines)
        # self.wait(time_gap)
        #
        # # 示例光线消失，画全部光线
        # self.play(FadeOut(lines))
        # create_action_lines, lines = \
        #     self.get_lines_1(radius_circle, num_all, dis_point, WIDTH_ENVELOPE, time_create)
        # self.play(*create_action_lines)
        # self.wait(time_gap)

        self.play(FadeOut(lines, circle, dot))
        self.wait(time_gap)

    def by_multiply_two(self):
        time_create_dots = 2
        time_create_lines = 3
        time_draw_line = 3
        radius_circle = 3
        num_demo = 30
        num_all = 200
        radius_dot_demo = 0.05
        radius_dot_all = 0.01

        dots1, lines1 = get_lines_2(num_demo, radius_circle, radius_dot_demo, WIDTH_BACK)
        dots2, lines2 = get_lines_2(num_all, radius_circle, radius_dot_all, WIDTH_ENVELOPE)

        # 生成点
        self.play(Create(dots1, run_time=time_create_dots))
        self.wait(time_gap)

        # 画线
        self.play(Create(lines1, run_time=time_create_lines))
        self.wait(time_gap)

        # 线消失，点增多
        self.play(FadeOut(lines1))
        self.play(ReplacementTransform(dots1, dots2))
        self.wait(time_gap)

        # 画线
        self.play(Create(lines2, run_time=time_create_lines * 2))
        self.wait(time_gap)

        # 画极坐标图像
        e = ValueTracker(0.01)
        plane = PolarPlane().add_coordinates().move_to(DOWN)
        graph = always_redraw(lambda: ParametricFunction(
            lambda t: plane.polar_to_point(2 * (1 + np.sin(t)), t),
            t_range=[0, e.get_value()], color=COLOR_BACK, stroke_width=WIDTH_BACK))
        self.add(graph)
        self.play(e.animate.set_value(2 * PI), run_time=time_draw_line, rate_func=linear)
        self.wait(time_gap)

        self.play(FadeOut(dots2, lines2))
        self.wait(time_gap)

    def by_rotate(self):
        radius_circle = 1

        circle_fix = Circle(radius=radius_circle, color=GREY, stroke_width=WIDTH_BACK)
        circle_mov = Circle(radius=radius_circle, color=GREY, stroke_width=WIDTH_BACK).rotate(PI)
        circle_mov.next_to(circle_fix, RIGHT, buff=0)
        circle_mov.start = circle_mov.copy()
        dot = Dot(circle_mov.point_from_proportion(0), color=ORANGE)
        line = Line(circle_mov.get_center(), dot.get_center(), color=GREY, stroke_width=WIDTH_ENVELOPE)
        path = VMobject(color=WHITE, stroke_width=WIDTH_BACK)
        path.set_points_as_corners([dot.get_center(), dot.get_center() + UP * 0.001])
        path_group = VGroup(line, dot, path)
        alpha = ValueTracker(0)

        def update_group(group):
            li, mob, pa = group
            mob.move_to(circle_mov.point_from_proportion(0))
            old_path = path.copy()
            old_path.append_vectorized_mobject(Line(old_path.points[-1], dot.get_center()))
            old_path.make_smooth()
            li.put_start_and_end_on(circle_mov.get_center(), dot.get_center())
            path.become(old_path)

        def update_mov(cir):
            cir.become(cir.start)
            cir.rotate(TAU * alpha.get_value(), about_point=circle_fix.get_center())
            cir.rotate(TAU * alpha.get_value(), about_point=cir.get_center())

        path_group.add_updater(update_group)
        circle_mov.add_updater(update_mov)

        self.play(Create(line), Create(circle_fix), Create(circle_mov), Create(dot))
        self.wait(time_gap)

        self.add(circle_mov, path_group)
        self.play(alpha.animate.set_value(1),
                  rate_func=linear,
                  run_time=7
                  )
        self.wait(time_gap)

        self.play(FadeOut(line, circle_fix, circle_mov, dot))
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
