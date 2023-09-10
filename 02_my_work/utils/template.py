# my_template.py
from manim import *


class SameScene(Scene):
    def __init__(self):
        super().__init__()
        self.plane = NumberPlane(
            background_line_style={
                "stroke_color": "#C2C2C2",
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        )

    def opening(self, title_words):
        self.camera.background_color = "#1C1C1C"

        self.add(self.plane)

        title = Tex(title_words).scale(3)
        self.play(Write(title), run_time=3)
        logo = MathTex(r"\mathbb{JAYANDJEAN}",
                       fill_color="#ece6e2").next_to(title, DOWN, buff=0.5).scale(2)
        self.play(Write(logo), run_time=2)
        self.wait()
        self.play(FadeOut(title))
        self.play(logo.animate.scale(0.4).move_to(RIGHT * 5.4 + UP * 3.2))
        self.wait(2)

    def caption(self, words):
        text = Text(words, font="Menlo", font_size=24).move_to(DOWN * 3.5)
        self.play(Write(text), run_time=2)
        return text
