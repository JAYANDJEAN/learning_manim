# my_template.py
from manim import *


class SameScene(Scene):
    def opening(self, title_words):
        PLANE = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        )
        self.add(PLANE)
        title = Tex(title_words).scale(3)
        self.play(Write(title), run_time=3)
        logo = MathTex(r"\mathbb{JAYANDJEAN}",
                       fill_color="#343434").next_to(title, DOWN, buff=0.5).scale(2)
        self.play(Write(logo), run_time=2)
        self.wait()
        self.play(FadeOut(title))
        self.play(logo.animate.scale(0.4).move_to(RIGHT * 5.4 + UP * 3.2))
        self.wait(2)
