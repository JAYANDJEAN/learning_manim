from helpers import *


class Parallelizability(Scene):
    def construct(self):
        comp_syms = (VGroup(*[MathTex(R"+\,\times").scale(0.7) for i in range(20)])
                     .arrange(DOWN).set(height=5).to_edge(DOWN))
        left_point = comp_syms.get_left() + 2 * LEFT
        right_point = comp_syms.get_right() + 2 * RIGHT
        curves = VGroup()
        for sym in comp_syms:
            curve = VMobject()
            curve.start_new_path(left_point)
            curve.add_cubic_bezier_curve_to(
                left_point + RIGHT,
                sym.get_left() + LEFT,
                sym.get_left()
            )
            curve.add_line_to(sym.get_right())
            curve.add_cubic_bezier_curve_to(
                sym.get_right() + RIGHT,
                right_point + LEFT,
                right_point,
            )
            curve.insert_n_curves(10)
            curves.add(curve)
        curves.set_stroke(width=0.5)
        curves.set_submobject_colors_by_gradient(TEAL, BLUE)

        # Setup words
        in_word = Text("Input")
        out_word = Text("output")
        in_word.next_to(left_point, LEFT, SMALL_BUFF)
        out_word.next_to(right_point, RIGHT, SMALL_BUFF)
        self.add(comp_syms, in_word, out_word)

        # GPU symbol
        gpu = SVGMobject("assets/gpu.svg").set_fill(GREY_B).set(width=1.0).next_to(comp_syms, UP)
        gpu_name = Text("GPU").scale(0.5).next_to(gpu, LEFT).set_fill(GREY_B)
        self.add(gpu, gpu_name)

        # Animation
        for n in range(4):
            curves.shuffle()
            self.play(
                LaggedStartMap(
                    ShowPassingFlash, curves,
                    lag_ratio=5e-3,
                    time_width=1.5,
                    run_time=4
                )
            )


if __name__ == "__main__":
    scene = Parallelizability()
    scene.render()
