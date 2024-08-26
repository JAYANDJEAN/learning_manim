import random

from helpers import *


class AttentionPatterns(MovingCameraScene):

    def construct(self):
        self.camera.background_color = "#1C1C1C"
        # 1. Add sentence
        phrase = " a fluffy blue creature roamed the verdant forest"
        words = list(filter(lambda s: s.strip(), phrase.split(" ")))
        word2mob = {word: Text(word) for word in words}
        word_mobs = VGroup(*word2mob.values()).arrange(RIGHT, buff=0.2).scale(0.7).move_to(2 * UP)

        self.play(LaggedStartMap(FadeIn, word_mobs, shift=0.5 * UP, lag_ratio=0.25))
        self.wait()

        # 2. Create word rects
        word2rect: Dict[str, VMobject] = dict()
        for word in word2mob:
            rect = SurroundingRectangle(word2mob[word], buff=-0.013)
            rect.set_stroke(GREY, 2)
            rect.set_fill(GREY, 0.2)
            rect.stretch_to_fit_height(0.55)
            rect.stretch_to_fit_width(rect.width + 0.15)
            rect.align_to(word2mob[word], RIGHT)
            word2rect[word] = rect

        ads = ["fluffy", "blue", "verdant"]
        nouns = ["creature", "forest"]
        others = ["a", "roamed", "the"]
        adj_mobs, noun_mobs, other_mobs = [
            VGroup(*[word2mob[substr] for substr in group])
            for group in (ads, nouns, others)]

        adj_rects, noun_rects, other_rects = [
            VGroup(*[word2rect[substr] for substr in group])
            for group in (ads, nouns, others)]
        adj_rects.set_submobject_colors_by_gradient(BLUE_C, BLUE_D, GREEN)

        noun_rects.set_color(GREY_BROWN).set_stroke(width=3)
        adj_arrows = VGroup(*[Arrow(adj_mobs[i].get_top(), noun_mobs[j].get_top(),
                                    path_arc=-150 * DEGREES, buff=0.1, stroke_color=GREY_B)
                              for i, j in [(0, 0), (1, 0), (2, 1)]])

        self.play(LaggedStartMap(DrawBorderThenFill, adj_rects), Animation(adj_mobs))
        self.wait()
        self.play(LaggedStartMap(DrawBorderThenFill, noun_rects), Animation(noun_mobs))
        self.play(LaggedStartMap(Create, adj_arrows, lag_ratio=0.2, run_time=2.0))
        # todo:不够美观
        self.play(ShowPassingFlash(adj_arrows.copy().set_color(BLUE), time_width=1, run_time=1.5))
        self.wait()

        # 3. Show embeddings
        all_rects = VGroup(*adj_rects, *noun_rects, *other_rects)
        all_rects.sort(lambda p: p[0])
        embeddings = VGroup(*[NumericEmbedding(length=10).set(width=0.5).next_to(rect, DOWN, buff=1.5)
                              for rect in all_rects])
        emb_arrows = VGroup(*[Arrow(all_rects[0].get_bottom(), embeddings[0].get_top()).match_x(rect)
                              for rect in all_rects])
        for index, vect in [(5, LEFT), (6, RIGHT)]:
            embeddings[index].shift(0.1 * vect)
            emb_arrows[index].shift(0.05 * vect)

        self.play(FadeIn(other_rects),
                  Animation(word_mobs),
                  LaggedStartMap(GrowArrow, emb_arrows),
                  LaggedStartMap(FadeIn, embeddings, shift=0.5 * DOWN),
                  FadeOut(adj_arrows))
        self.wait()

        # 4. Mention dimension of embedding
        brace = Brace(embeddings[0], LEFT, buff=SMALL_BUFF)
        dim_value = Integer(12288)
        dim_value.next_to(brace, LEFT)
        dim_value.set_color(YELLOW)

        self.play(GrowFromCenter(brace), Create(dim_value), self.camera.frame.animate.shift(LEFT))
        self.wait()

        # 5. Ingest meaning and and position
        images = Group(*[ImageMobject(f"assets/image.png").set(height=0.8).next_to(word2rect[word], UP)
                         for word in ["fluffy", "blue", "creature", "verdant", "forest"]])
        image_embeddings = VGroup(*[embeddings[i] for i in [1, 2, 3, 6, 7]])
        self.play(LaggedStartMap(FadeIn, images, scale=2, lag_ratio=0.05))
        self.play(LaggedStart((bake_mobject_into_vector_entries(image, embed)
                               for image, embed in zip(images, image_embeddings)),
                              lag_ratio=0.2,
                              run_time=4))
        self.add(embeddings)

        # 6. Show positions
        pos_labels = VGroup(*[Integer(n, font_size=36).next_to(rect, DOWN, buff=0.1)
                              for n, rect in enumerate(all_rects, start=1)])
        pos_labels.set_color(TEAL)
        arrow_group = AnimationGroup(arrow.animate.scale(0.7, about_edge=DOWN)
                                     for arrow in emb_arrows)
        self.play(LaggedStart(arrow_group, lag_ratio=0.1),
                  LaggedStartMap(FadeIn, pos_labels, shift=0.25 * DOWN, lag_ratio=0.1))
        self.play(LaggedStart((bake_mobject_into_vector_entries(pos, embed)
                               for pos, embed in zip(pos_labels, embeddings)),
                              lag_ratio=0.2,
                              run_time=4))
        self.wait()

        # 7. Collapse vectors
        emb_syms = VGroup()
        for n, rect in enumerate(all_rects, start=1):
            sym = MathTex(f"\\vec{{E}}_{{{n}}}")
            sym.next_to(rect, DOWN, buff=0.75)
            sym.set_color(GREY_A)
            emb_syms.add(sym)

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

        all_brackets = VGroup(*[emb.get_brackets() for emb in embeddings])
        for brackets in all_brackets:
            brackets.target = brackets.generate_target()
            brackets.target.stretch(0, 1, about_edge=UP)
            brackets.target.set_fill(opacity=0)

        ghost_syms = emb_syms.copy()
        ghost_syms.set_opacity(0)

        self.play(
            self.camera.frame.animate.set_x(0),
            LaggedStart(
                (AnimationGroup(
                    LaggedStart(
                        (FadeTransform(entry, sym)
                         for entry in embedding.get_columns()[0]),
                        lag_ratio=0.01,
                        group_type=Group
                    ),
                    MoveToTarget(brackets),
                    group_type=Group,
                )
                    for sym, embedding, brackets in zip(ghost_syms, embeddings, all_brackets)),
                group_type=Group,
                run_time=2
            ),
            LaggedStartMap(FadeIn, emb_syms, shift=UP),
            brace.animate.stretch(0.25, 1, about_edge=UP).set_opacity(0),
            FadeOut(dim_value, shift=0.25 * UP),
            MoveToTarget(emb_arrows, lag_ratio=0.1, run_time=2),
            LaggedStartMap(FadeOut, pos_labels, shift=UP),
        )
        self.clear()
        self.add(emb_arrows, all_rects, word_mobs, images, emb_syms)
        self.wait()

        # 8. Preview desired updates
        emb_sym_primes = VGroup(*[sym.copy().add(MathTex("'").move_to(sym.get_corner(UR) + 0.05 * DL))
                                  for sym in emb_syms])
        emb_sym_primes.shift(2 * DOWN)
        emb_sym_primes.set_color(TEAL)

        full_connections = VGroup()
        for i, sym1 in enumerate(emb_syms, start=1):
            for j, sym2 in enumerate(emb_sym_primes, start=1):
                line = Line(sym1.get_bottom(), sym2.get_top(), buff=SMALL_BUFF)
                line.set_stroke(GREY_B, width=random.random() ** 2, opacity=random.random() ** 0.25)
                if (i, j) in [(2, 4), (3, 4), (4, 4), (7, 8), (8, 8)]:
                    line.set_stroke(WHITE, width=2 + random.random(), opacity=1)
                full_connections.add(line)

        blue_fluff = ImageMobject("assets/image.png")
        verdant_forest = ImageMobject("assets/image.png")
        for n, image in [(3, blue_fluff), (7, verdant_forest)]:
            image.match_height(images)
            image.scale(1.2)
            image.next_to(emb_sym_primes[n], DOWN, buff=MED_SMALL_BUFF)

        self.play(
            Create(full_connections, lag_ratio=0.01, run_time=2),
            LaggedStart(
                (TransformFromCopy(sym1, sym2)
                 for sym1, sym2 in zip(emb_syms, emb_sym_primes)),
                lag_ratio=0.05,
                run_time=4
            ),
        )
        self.wait()

        fade_group = AnimationGroup([FadeTransform(im.copy(), blue_fluff) for im in images[:3]] +
                                    [FadeTransform(im.copy(), verdant_forest) for im in images[3:]])
        self.play(LaggedStart(fade_group, lag_ratio=0.5, run_time=2))
        self.wait()

        # 9. Show black box that matrix multiples can be added to
        in_arrows = VGroup(*[Vector(0.25 * DOWN).next_to(sym, DOWN, SMALL_BUFF)
                             for sym in emb_syms])
        box = Rectangle(width=15.0, height=3.0)
        box.set_fill(GREY_E, 1)
        box.set_stroke(WHITE, 1)
        box.next_to(in_arrows, DOWN, SMALL_BUFF)
        out_arrows = in_arrows.copy()
        out_arrows.next_to(box, DOWN)

        self.play(
            FadeIn(box, shift=0.25 * DOWN),
            LaggedStartMap(FadeIn, in_arrows, shift=0.25 * DOWN, lag_ratio=0.025),
            LaggedStartMap(FadeIn, out_arrows, shift=0.25 * DOWN, lag_ratio=0.025),
            FadeOut(full_connections),
            emb_sym_primes.animate.next_to(out_arrows, DOWN, SMALL_BUFF),
            MaintainPositionRelativeTo(blue_fluff, emb_sym_primes),
            MaintainPositionRelativeTo(verdant_forest, emb_sym_primes),
            self.camera.frame.animate.set_height(10).move_to(4 * UP, UP),
        )
        self.wait()

        # 10. Clear the board
        self.play(
            self.camera.frame.animate.set_height(8).move_to(2 * UP),
            LaggedStartMap(FadeOut, Group(
                *images, in_arrows, box, out_arrows, emb_sym_primes,
                blue_fluff, verdant_forest,
            ), lag_ratio=0.1)
        )

        # 11. Ask questions
        word_groups = VGroup(*[VGroup(*pair) for pair in zip(all_rects, word_mobs)])
        for group in word_groups:
            group.save_state()

        text_q = Text("Any adjectives \nin front of me?").scale(0.5)
        text_q.move_to(word2rect["creature"].get_top() + 0.5 * UP)
        text_a = Text("I am!").scale(0.5)
        text_a.move_to(word2rect["fluffy"].get_top() + 0.5 * UP)

        self.play(FadeIn(text_q),
                  word_groups[:3].animate.fade(0.75),
                  word_groups[4:].animate.fade(0.75))
        self.wait()
        self.play(LaggedStart(
            Restore(word_groups[1]),
            Restore(word_groups[2]),
            Write(text_a),
            lag_ratio=0.5
        ))
        self.wait()

        # 12. Associate questions with vectors
        text_a.save_state()
        q_arrows = VGroup(*[Vector(0.75 * DOWN).next_to(sym, DOWN, SMALL_BUFF)
                            for sym in emb_syms])
        q_vects = VGroup(*[NumericEmbedding(length=7).set(height=2).next_to(arrow, DOWN)
                           for arrow in q_arrows])

        index = words.index("creature")
        q_vect = q_vects[index]
        q_arrow = q_arrows[index]
        self.play(LaggedStart(
            text_q.animate.scale(0.75).next_to(q_vect, RIGHT),
            FadeIn(q_vect, shift=DOWN),
            GrowArrow(q_arrow),
            self.camera.frame.animate.move_to(ORIGIN),
            text_a.animate.fade(0.5),
        ))
        self.play(bake_mobject_into_vector_entries(text_q, q_vect))
        self.wait()

        # 13. Label query vector
        brace = Brace(q_vect, LEFT, SMALL_BUFF)
        query_word = Text("Query")
        query_word.set_color(YELLOW)
        query_word.next_to(brace, LEFT, SMALL_BUFF)
        dim_text = Text("128-dimensional", font_size=36)
        dim_text.set_color(YELLOW)
        dim_text.next_to(brace, LEFT, SMALL_BUFF)
        dim_text.set_y(query_word.get_y(DOWN))

        self.play(GrowFromCenter(brace), FadeIn(query_word, shift=0.25 * LEFT))
        self.wait()
        self.play(query_word.animate.next_to(dim_text, UP, SMALL_BUFF),
                  FadeIn(dim_text, shift=0.1 * DOWN))
        self.wait()

        # 14. Show individual matrix product
        e_vect = NumericEmbedding(length=12).match_width(q_vect)
        e_vect.next_to(q_vect, DR, buff=1.5)
        matrix = WeightMatrix(shape=(7, 12)).match_height(q_vect)
        matrix.next_to(e_vect, LEFT)
        e_label_copy = emb_syms[index].copy()
        e_label_copy.next_to(e_vect, UP)
        q_vect.save_state()
        ghost_q_vect = NumericEmbedding(length=7).match_height(q_vect)
        ghost_q_vect.get_columns().set_opacity(0)
        ghost_q_vect.get_brackets().space_out_submobjects(1.75)
        ghost_q_vect.next_to(e_vect, RIGHT, buff=0.7)

        mat_brace = Brace(matrix, UP)
        mat_label = MathTex("W_Q")
        mat_label.next_to(mat_brace, UP, SMALL_BUFF)
        mat_label.set_color(YELLOW)

        self.play(
            self.camera.frame.animate.set_height(11).move_to(all_rects, UP).shift(0.35 * UP),
            FadeOut(text_a),
            FadeIn(e_vect),
            FadeIn(matrix),
            TransformFromCopy(emb_syms[index], e_label_copy),
            FadeOut(q_vect),
            TransformFromCopy(q_vect, ghost_q_vect),
            MaintainPositionRelativeTo(text_q, q_vect),
        )
        self.play(
            GrowFromCenter(mat_brace),
            FadeIn(mat_label, shift=0.1 * UP),
        )
        # todo
        # self.remove(ghost_q_vect)
        # eq, rhs = show_matrix_vector_product(self, matrix, e_vect)

        rhs = ghost_q_vect
        ghost_q_vect.get_columns().set_opacity(1.0)

        new_q_vect = rhs.match_width(q_vect).copy()
        new_q_vect.move_to(q_vect, LEFT)

        self.play(
            TransformFromCopy(rhs, new_q_vect, path_arc=PI / 2),
            text_q.animate.next_to(new_q_vect, RIGHT)
        )
        self.wait()

        # 15. Collapse query vector
        # q_syms = VGroup()
        # for n, arrow in enumerate(q_arrows, start=1):
        #     sym = MathTex(f"\\vec{{Q}}_{{{n}}}", font_size=48)
        #     sym.next_to(arrow, DOWN, SMALL_BUFF)
        #     q_syms.add(sym)
        #
        # mat_label2 = mat_label.copy()
        #
        # q_sym = q_syms[index]
        # low_q_sym = q_sym.copy()
        # low_q_sym.next_to(rhs, UP)
        #
        # self.play(LaggedStart(
        #     LaggedStart(
        #         (FadeTransform(entry, q_sym, remover=True)
        #          for entry in new_q_vect.get_columns()[0]),
        #         lag_ratio=0.01,
        #         group_type=Group,
        #     ),
        #     new_q_vect.get_brackets().animate.stretch(0, 1, about_edge=UP).set_opacity(0),
        #     FadeOut(query_word, target_position=q_sym.get_center()),
        #     FadeOut(dim_text, target_position=q_sym.get_center()),
        #     FadeOut(brace),
        #     text_q.animate.next_to(q_sym, DOWN),
        #     FadeIn(low_q_sym, UP),
        #     lag_ratio=0.1,
        # ))
        # self.remove(new_q_vect)
        # self.add(q_sym)
        # self.play(
        #     mat_label2.animate.scale(0.9).next_to(q_arrow, RIGHT, buff=0.15),
        # )
        # self.wait()


if __name__ == "__main__":
    scene = AttentionPatterns()
    scene.render()
