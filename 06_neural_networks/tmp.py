from utils import *


class test_dash(Scene):
    def construct(self):
        def dash_updater(mob):
            offset = vt.get_value()
            mob['dashes'].become(mob.dash_objects(num_dashes, dash_ratio=0.5, offset=offset))

        plane = NumberPlane(
            background_line_style={
                "stroke_color": "#C2C2C2",
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        )
        mob1 = CubicBezier(3 * LEFT, UP, DOWN, 3 * RIGHT)
        vt = ValueTracker(0)
        num_dashes = 8
        speed = 7

        dash1 = DashedMObject(mob1, num_dashes=num_dashes, dashed_ratio=0.5, dash_offset=0)
        dash1.add_updater(dash_updater)

        self.add(plane, dash1)
        self.play(vt.animate.set_value(speed), run_time=6)
        self.wait()


if __name__ == "__main__":
    scene = test_dash()
    scene.render()