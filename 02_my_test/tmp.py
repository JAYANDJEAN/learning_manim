from manim import *


class EllipseReflection(Scene):
    def construct(self):
        # 创建椭圆
        ellipse = Ellipse(width=4, height=2, color=BLUE)
        ellipse.move_to(ORIGIN)

        # 创建光源
        light_source = Dot(color=YELLOW)
        light_source.move_to(ellipse.point_from_proportion(0.3))  # 初始位置在椭圆内

        # 创建入射光线
        incident_ray = Line(light_source.get_center(), ellipse.get_center(), color=YELLOW)
        incident_ray.set_stroke(width=2)

        # 创建反射光线
        reflected_ray = Line(ellipse.get_center(), 2 * RIGHT, color=GREEN)
        reflected_ray.set_stroke(width=2)

        # 显示椭圆、光源和入射光线
        self.play(Create(ellipse))
        self.play(Create(light_source))
        self.play(Create(incident_ray))

        # 添加反射动画
        self.wait(0.5)
        self.play(Transform(incident_ray, reflected_ray))

        self.wait(1)
