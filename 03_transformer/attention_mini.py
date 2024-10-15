from manim import *


class Attention(MovingCameraScene):
    def construct(self):
        phrase = " a fluffy blue creature roamed the verdant forest"
        text_words = VGroup(*[Text(word) for word in phrase.strip().split(" ")])
        text_words.arrange(RIGHT, buff=0.2).scale(0.7).move_to(2 * UP)
        rect_words = VGroup()
        for word in text_words:
            rect = SurroundingRectangle(word, buff=-0.013).set_stroke(GREY, 2).set_fill(GREY, 0.2)
            rect.stretch_to_fit_height(0.55)
            rect.stretch_to_fit_width(rect.width + 0.15)
            rect.align_to(word, RIGHT)
            rect_words.add(rect)
        sym_q = VGroup(*[
            MathTex(f"\\vec{{Q}}_{{{i}}}", font_size=48).next_to(rect_words[i], DOWN, buff=1.0)
            for i in range(len(text_words))])
        arrows_q = VGroup(*[Arrow(rect_words[i].get_bottom(), sym_q[i].get_top(), buff=0.1)
                            for i in range(len(rect_words))])
        rect_words.set_submobject_colors_by_gradient(BLUE_C, BLUE_D, GREEN)
        all_q = VGroup(text_words, rect_words, arrows_q, sym_q)

        self.play(LaggedStartMap(FadeIn, text_words, shift=0.5 * UP, lag_ratio=0.25))
        self.play(LaggedStartMap(DrawBorderThenFill, rect_words))
        self.play(LaggedStartMap(GrowArrow, arrows_q, lag_ratio=0.25),
                  LaggedStartMap(Write, sym_q, lag_ratio=0.25))
        self.play(all_q.animate.scale(0.7).move_to(3 * UP + 1 * RIGHT))

        self.wait()

        key_words = VGroup(*[VGroup(text_words[i].copy(), rect_words[i].copy()) for i in range(len(text_words))])
        key_words.arrange(DOWN, buff=0.75, aligned_edge=RIGHT).next_to(sym_q, DL, buff=LARGE_BUFF).shift(3.0 * LEFT)
        sym_k = VGroup(*[
            MathTex(f"\\vec{{K}}_{{{i}}}", font_size=48).next_to(key_words[i], RIGHT, buff=1.0)
            for i in range(len(key_words))])
        arrows_k = VGroup(*[Arrow(key_words[i].get_right(), sym_k[i].get_left(), buff=0.1)
                            for i in range(len(key_words))])

        h_lines = VGroup()
        v_buff = 0.5 * (key_words[0].get_y(DOWN) - key_words[1].get_y(UP))
        for kwg in key_words:
            h_line = Line(LEFT, RIGHT).set(width=20)
            h_line.next_to(kwg, UP, buff=v_buff)
            h_line.align_to(key_words, LEFT)
            h_lines.add(h_line)

        v_lines = VGroup()
        h_buff = 0.5
        for q_group in text_words:
            v_line = Line(UP, DOWN).set(height=14)
            v_line.next_to(q_group, LEFT, buff=h_buff, aligned_edge=UP)
            v_lines.add(v_line)
        v_lines.add(v_lines[-1].copy().next_to(q_group, RIGHT, 0.5, UP))

        grid_lines = VGroup(*h_lines, *v_lines)
        grid_lines.set_stroke(GREY_A, 1)

        self.play(
            Create(key_words),
            Create(arrows_k), Create(sym_k),
            Create(h_lines, lag_ratio=0.2),
            Create(v_lines, lag_ratio=0.2),
        )


if __name__ == "__main__":
    scene = Attention()
    scene.render()
