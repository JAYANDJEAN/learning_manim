import random

from helpers import *


class Test(MovingCameraScene):

    def construct(self):
        self.camera.background_color = "#1C1C1C"

        phrase = " a fluffy blue creature roamed the verdant forest"
        words = list(filter(lambda s: s.strip(), phrase.split(" ")))
        word2mob = {word: Text(word) for word in words}
        word_mobs = VGroup(*word2mob.values()).arrange(RIGHT, buff=0.2).scale(0.7).move_to(2 * UP)

        word2rect: Dict[str, VMobject] = dict()
        for word in word2mob:
            rect = SurroundingRectangle(word2mob[word], buff=-0.013).set_stroke(GREY, 2).set_fill(GREY, 0.2)
            rect.stretch_to_fit_height(0.55)
            rect.stretch_to_fit_width(rect.width + 0.15)
            rect.align_to(word2mob[word], RIGHT)
            word2rect[word] = rect
        all_rects = VGroup(*word2rect.values())
        embeddings = VGroup(*[NumericEmbedding(length=10).set(width=0.5).next_to(rect, DOWN, buff=1.5)
                              for rect in all_rects])
        emb_arrows = VGroup(*[Arrow(all_rects[i].get_bottom(), embeddings[i].get_top())
                              for i in range(len(all_rects))])
        emb_syms = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}").next_to(rect, DOWN, buff=0.75).set_color(GREY_A)
                            for n, rect in enumerate(all_rects)])

        emb_arrows.target = emb_arrows.generate_target()
        for rect, arrow, sym in zip(all_rects, emb_arrows.target, emb_syms):
            x_min = rect.get_x(LEFT)
            x_max = rect.get_x(RIGHT)
            low_point = sym.get_top()
            if x_min < low_point[0] < x_max:
                top_point = np.array([low_point[0], rect.get_y(DOWN), 0])
            else:
                top_point = rect.get_bottom()
            arrow.become(Arrow(top_point, low_point, buff=SMALL_BUFF))

        self.play(LaggedStartMap(FadeIn, word_mobs, shift=0.5 * UP, lag_ratio=0.25))
        self.play(LaggedStartMap(DrawBorderThenFill, all_rects))
        self.play(LaggedStartMap(GrowArrow, emb_arrows),
                  LaggedStartMap(FadeIn, embeddings, shift=0.5 * DOWN))
        self.wait()

        self.play(
            LaggedStart(
                AnimationGroup(
                    Transform(embed, sym)
                    for sym, embed in zip(emb_syms, embeddings)
                ),
                group_type=Group,
                run_time=2
            ),
            MoveToTarget(emb_arrows, lag_ratio=0.1, run_time=2),
        )
        self.wait()


if __name__ == "__main__":
    scene = Test()
    scene.render()
