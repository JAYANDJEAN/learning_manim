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
            rect = SurroundingRectangle(word2mob[word], buff=-0.013).set_stroke(GREY, 2).set_fill(GREY, 0.2)
            rect.stretch_to_fit_height(0.55)
            rect.stretch_to_fit_width(rect.width + 0.15)
            rect.align_to(word2mob[word], RIGHT)
            word2rect[word] = rect

        word_group = [["fluffy", "blue", "verdant"], ["creature", "forest"], ["a", "roamed", "the"]]
        adj_mobs, noun_mobs, other_mobs = [VGroup(*[word2mob[substr] for substr in group]) for group in word_group]
        adj_rects, noun_rects, other_rects = [VGroup(*[word2rect[substr] for substr in group]) for group in word_group]
        adj_rects.set_submobject_colors_by_gradient(BLUE_C, BLUE_D, GREEN)
        noun_rects.set_color(GREY_BROWN).set_stroke(width=3)
        adj_arrows = VGroup(*[Arrow(adj_mobs[i].get_top(), noun_mobs[j].get_top(),
                                    path_arc=-150 * DEGREES, buff=0.1, stroke_color=GREY_B)
                              for i, j in [(0, 0), (1, 0), (2, 1)]])

        self.play(LaggedStartMap(DrawBorderThenFill, adj_rects), Animation(adj_mobs))
        self.wait()
        self.play(LaggedStartMap(DrawBorderThenFill, noun_rects), Animation(noun_mobs))
        self.play(LaggedStartMap(GrowArrow, adj_arrows, lag_ratio=0.2, run_time=2.0))
        # todo:不够美观
        self.play(ShowPassingFlash(adj_arrows.copy().set_color(BLUE), time_width=1, run_time=1.5))
        self.wait()

        # 3. Show embeddings
        all_rects = VGroup(*adj_rects, *noun_rects, *other_rects)
        all_rects.sort(lambda p: p[0])
        embeddings = VGroup(*[WeightMatrix(length=10).set(width=0.5).next_to(rect, DOWN, buff=1.5)
                              for rect in all_rects])
        emb_arrows = VGroup(*[Arrow(all_rects[i].get_bottom(), embeddings[i].get_top())
                              for i in range(len(all_rects))])
        self.play(FadeIn(other_rects),
                  Animation(word_mobs),
                  LaggedStartMap(GrowArrow, emb_arrows),
                  LaggedStartMap(FadeIn, embeddings, shift=0.5 * DOWN),
                  FadeOut(adj_arrows))
        self.wait()

        # 4. Mention dimension of embedding
        brace = Brace(embeddings[0], LEFT, buff=SMALL_BUFF)
        dim_value = Integer(12288).next_to(brace, LEFT).set_color(YELLOW)

        self.play(GrowFromCenter(brace),
                  Create(dim_value),
                  self.camera.frame.animate.shift(LEFT)
                  )
        self.wait()

        # 5. Ingest meaning and and position
        images = Group(*[ImageMobject(f"assets/image.png").set(height=0.8).next_to(word2rect[word], UP)
                         for word in ["fluffy", "blue", "creature", "verdant", "forest"]])
        image_embeddings = VGroup(*[embeddings[i] for i in [1, 2, 3, 6, 7]])
        self.play(LaggedStartMap(FadeIn, images, scale=2, lag_ratio=0.05))
        self.play(LaggedStart(*[bake_mobject_into_vector_entries(image, embed)
                                for image, embed in zip(images, image_embeddings)],
                              lag_ratio=0.2,
                              run_time=4))
        self.add(embeddings)

        # 6. Show positions
        pos_labels = VGroup(*[Integer(n, font_size=36).next_to(rect, DOWN, buff=0.1)
                              for n, rect in enumerate(all_rects, start=1)])
        pos_labels.set_color(TEAL)

        self.play(
            LaggedStart(
                AnimationGroup(arrow.animate.scale(0.7, about_edge=DOWN)
                               for arrow in emb_arrows),
                lag_ratio=0.1),
            LaggedStartMap(FadeIn, pos_labels, shift=0.25 * DOWN, lag_ratio=0.1)
        )
        self.play(
            LaggedStart(*[bake_mobject_into_vector_entries(pos, embed)
                          for pos, embed in zip(pos_labels, embeddings)],
                        lag_ratio=0.2,
                        run_time=4)
        )
        self.wait()

        # 7. Collapse vectors
        emb_syms = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}").next_to(rect, DOWN, buff=0.75).set_color(GREY_A)
                            for n, rect in enumerate(all_rects, start=1)])
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
        self.play(self.camera.frame.animate.set_x(0))
        self.play(
            LaggedStart(*[Transform(embed, sym)
                          for sym, embed in zip(emb_syms, embeddings)],
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
            LaggedStart(*[TransformFromCopy(sym1, sym2) for sym1, sym2 in zip(emb_syms, emb_sym_primes)],
                        lag_ratio=0.05,
                        run_time=4),
        )
        self.wait()

        fade_group = AnimationGroup([FadeTransform(im.copy(), blue_fluff) for im in images[:3]] +
                                    [FadeTransform(im.copy(), verdant_forest) for im in images[3:]])
        self.play(LaggedStart(fade_group, lag_ratio=0.5, run_time=2))
        self.wait()

        # 9. Show black box that matrix multiples can be added to
        in_arrows = VGroup(*[Vector(0.25 * DOWN).next_to(sym, DOWN, SMALL_BUFF)
                             for sym in emb_syms])
        box = Rectangle(width=15.0, height=3.0).set_fill(GREY_E, 1).set_stroke(WHITE, 1)
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
        q_vects = VGroup(*[WeightMatrix(length=7).set(height=2).next_to(arrow, DOWN)
                           for arrow in q_arrows])

        index = words.index("creature")
        q_vect = q_vects[index]
        q_arrow = q_arrows[index]
        self.play(
            LaggedStart(
                AnimationGroup(
                    text_q.animate.scale(0.75).next_to(q_vect, RIGHT),
                    FadeIn(q_vect, shift=DOWN),
                    GrowArrow(q_arrow),
                    self.camera.frame.animate.move_to(ORIGIN),
                    text_a.animate.fade(0.5)
                )
            )
        )
        self.play(bake_mobject_into_vector_entries(text_q, q_vect))
        self.wait()

        # 13. Label query vector
        brace = Brace(q_vect, LEFT, SMALL_BUFF)
        query_word = Text("Query").set_color(YELLOW).next_to(brace, LEFT, SMALL_BUFF)
        dim_text = Text("128-dimensional", font_size=36).set_color(YELLOW).next_to(brace, LEFT, SMALL_BUFF)
        dim_text.set_y(query_word.get_y(DOWN))

        self.play(GrowFromCenter(brace), FadeIn(query_word, shift=0.25 * LEFT))
        self.wait()
        self.play(query_word.animate.next_to(dim_text, UP, SMALL_BUFF),
                  FadeIn(dim_text, shift=0.1 * DOWN))
        self.wait()

        # 14. Show individual matrix product
        e_vect = WeightMatrix(length=12).match_width(q_vect).next_to(q_vect, DR, buff=1.5)
        matrix = WeightMatrix(shape=(7, 12)).match_height(q_vect).next_to(e_vect, LEFT)
        rhs = WeightMatrix(length=7).match_width(q_vect).next_to(e_vect, RIGHT, buff=0.7)
        e_label_copy = emb_syms[index].copy().next_to(e_vect, UP)

        q_vect.save_state()

        rhs.get_columns().set_opacity(0)
        rhs.get_brackets().space_out_submobjects(1.75)
        mat_brace = Brace(matrix, UP)
        mat_label = MathTex("W_Q").next_to(mat_brace, UP, SMALL_BUFF).set_color(YELLOW)

        self.play(
            self.camera.frame.animate.set_height(11).move_to(all_rects, UP).shift(0.35 * UP),
            FadeOut(text_a),
            FadeIn(e_vect),
            FadeIn(matrix),
            TransformFromCopy(emb_syms[index], e_label_copy),
            FadeOut(q_vect),
            FadeIn(rhs),
            MaintainPositionRelativeTo(text_q, q_vect),
        )
        self.play(
            GrowFromCenter(mat_brace),
            FadeIn(mat_label, shift=0.1 * UP),
        )
        self.play(
            rhs.animate.set_opacity(1.0),
            TransformFromCopy(rhs, q_vect, path_arc=PI / 2),
            text_q.animate.next_to(q_vect, RIGHT)
        )
        self.wait()

        # 15. Collapse query vector
        q_syms = VGroup()
        for n, arrow in enumerate(q_arrows, start=1):
            sym = MathTex(f"\\vec{{Q}}_{{{n}}}", font_size=48)
            sym.next_to(arrow, DOWN, SMALL_BUFF)
            q_syms.add(sym)

        mat_label2 = mat_label.copy()
        q_sym = q_syms[index]
        low_q_sym = q_sym.copy()
        low_q_sym.next_to(rhs, UP)

        self.play(
            LaggedStart(
                LaggedStart(*[FadeTransform(entry, q_sym, remover=True)
                              for entry in q_vect.get_columns()[0]],
                            lag_ratio=0.01,
                            group_type=Group,
                            ),
                q_vect.get_brackets().animate.stretch(0, 1, about_edge=UP).set_opacity(0),
                FadeOut(query_word, target_position=q_sym.get_center()),
                FadeOut(dim_text, target_position=q_sym.get_center()),
                FadeOut(brace),
                lag_ratio=0.1,
            ))
        self.add(q_arrows, q_syms)
        self.play(FadeOut(text_q, e_vect, matrix, rhs, mat_label, mat_brace, e_label_copy))
        self.wait()

        # 16. E to Q rects

        # 17. Add other query vectors

        # Draw grid
        key_word_groups = word_groups.copy()
        key_word_groups.arrange(DOWN, buff=0.75, aligned_edge=RIGHT)
        key_word_groups.next_to(q_syms, DL, buff=LARGE_BUFF)
        key_word_groups.shift(3.0 * LEFT)
        q_groups = VGroup(
            *[VGroup(*[group[i] for group in [emb_arrows, emb_syms, q_arrows, q_syms]])
              for i in range(len(emb_arrows))]
        )
        q_groups.target = q_groups.generate_target()
        q_groups.target.arrange_to_fit_width(12, about_edge=LEFT)
        q_groups.target.shift(0.25 * DOWN)

        word_groups.target = word_groups.generate_target()
        for word_group, q_group in zip(word_groups.target, q_groups.target):
            word_group.scale(0.7)
            word_group.next_to(q_group[0], UP, SMALL_BUFF)

        h_lines = VGroup()
        v_buff = 0.5 * (key_word_groups[0].get_y(DOWN) - key_word_groups[1].get_y(UP))
        for kwg in key_word_groups:
            h_line = Line(LEFT, RIGHT).set_width(20)
            h_line.next_to(kwg, UP, buff=v_buff)
            h_line.align_to(key_word_groups, LEFT)
            h_lines.add(h_line)

        v_lines = VGroup()
        h_buff = 0.5
        for q_group in q_groups.target:
            v_line = Line(UP, DOWN).set_height(14)
            v_line.next_to(q_group, LEFT, buff=h_buff, aligned_edge=UP)
            v_lines.add(v_line)
        v_lines.add(v_lines[-1].copy().next_to(q_groups.target, RIGHT, 0.5, UP))

        grid_lines = VGroup(*h_lines, *v_lines)
        grid_lines.set_stroke(GREY_A, 1)

        self.play(
            self.camera.frame.animate.set_height(15, about_edge=UP).set_x(-2),
            MoveToTarget(q_groups),
            MoveToTarget(word_groups),
            Create(h_lines, lag_ratio=0.2),
            Create(v_lines, lag_ratio=0.2),
        )

        # Take all dot products
        # dot_prods = VGroup()
        # for k_sym in k_syms:
        #     for q_sym in q_syms:
        #         square_center = np.array([q_sym.get_x(), k_sym.get_y(), 0])
        #         dot = Tex(R".", font_size=72)
        #         dot.move_to(square_center)
        #         dot.set_fill(opacity=0)
        #         dot_prod = VGroup(k_sym.copy(), dot, q_sym.copy())
        #         dot_prod.target = dot_prod.generate_target()
        #         dot_prod.target.arrange(RIGHT, buff=0.15)
        #         dot_prod.target.scale(0.65)
        #         dot_prod.target.move_to(square_center)
        #         dot_prod.target.set_fill(opacity=1)
        #         dot_prods.add(dot_prod)
        #
        # self.play(
        #     LaggedStartMap(MoveToTarget, dot_prods, lag_ratio=0.025, run_time=4)
        # )
        # self.wait()


if __name__ == "__main__":
    scene = AttentionPatterns()
    scene.render()
