from manimlib import *


class MultiHeadedAttention(InteractiveScene):
    def construct(self):
        # Mention head
        background_rect = FullScreenRectangle()
        single_title = Text("Single head of attention")
        multiple_title = Text("Multi-headed attention")
        titles = VGroup(single_title, multiple_title)
        for title in titles:
            title.scale(1.25)
            title.to_edge(UP)

        screen_rect = ScreenRectangle(height=6)
        screen_rect.set_fill(BLACK, 1)
        screen_rect.set_stroke(WHITE, 3)
        screen_rect.next_to(titles, DOWN, buff=0.5)

        head = single_title["head"][0]

        self.add(background_rect)
        self.add(single_title)
        self.add(screen_rect)
        self.wait()
        self.play(
            FlashAround(head, run_time=2),
            head.animate.set_color(YELLOW),
        )
        self.wait()

        # Change title
        kw = dict(path_arc=45 * DEGREES)
        self.play(
            FadeTransform(single_title["Single"], multiple_title["Multi-"], **kw),
            FadeTransform(single_title["head"], multiple_title["head"], **kw),
            FadeIn(multiple_title["ed"], 0.25 * RIGHT),
            FadeTransform(single_title["attention"], multiple_title["attention"], **kw),
            FadeOut(single_title["of"])
        )
        self.add(multiple_title)

        # Set up images
        n_heads = 15
        # directory = "/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2024/transformers/attention/images/"
        heads = Group()
        for n in range(n_heads):
            im = ImageMobject("assets/prompt.png")
            im.set_opacity(1)
            im.shift(0.01 * OUT)
            rect = SurroundingRectangle(im, buff=0)
            rect.set_fill(BLACK, 0.75)
            rect.set_stroke(WHITE, 1, 1)
            heads.add(Group(rect, im))

        # Show many parallel layers
        self.set_floor_plane("xz")
        frame = self.frame
        multiple_title.fix_in_frame()
        background_rect.fix_in_frame()

        heads.set_height(4)
        heads.arrange(OUT, buff=1.0)
        heads.move_to(DOWN)
        pre_head = ImageMobject("assets/prompt.png")

        pre_head.replace(screen_rect)
        pre_head = Group(screen_rect, pre_head)

        self.add(pre_head)
        self.wait()
        self.play(
            frame.animate.reorient(41, -12, 0, (-1.0, -1.42, 1.09), 12.90).set_anim_args(run_time=2),
            background_rect.animate.set_fill(opacity=0.75),
            FadeTransform(pre_head, heads[-1], time_span=(1, 2)),
        )
        self.play(
            frame.animate.reorient(48, -11, 0, (-1.0, -1.42, 1.09), 12.90),
            LaggedStart(
                (FadeTransform(heads[-1].copy(), image)
                 for image in heads),
                lag_ratio=0.1,
                group_type=Group,
            ),
            run_time=4,
        )
        self.add(heads)
        self.wait()

        # Show matrices
        colors = [YELLOW, TEAL, RED, PINK]
        texs = ["W_Q", "W_K", R"\downarrow W_V", R"\uparrow W_V"]
        n_shown = 9
        wq_syms, wk_syms, wv_down_syms, wv_up_syms = sym_groups = VGroup(
            VGroup(
                Tex(tex + f"^{{({n})}}", font_size=36).next_to(image, UP, MED_SMALL_BUFF)
                for n, image in enumerate(heads[:-n_shown - 1:-1], start=1)
            ).set_color(color).set_backstroke(BLACK, 5)
            for tex, color in zip(texs, colors)
        )
        for group in wv_down_syms, wv_up_syms:
            for sym in group:
                sym[0].next_to(sym[1], LEFT, buff=0.025)
        dots = Tex(R"\dots", font_size=90)
        dots.rotate(PI / 2, UP)
        sym_rot_angle = 70 * DEGREES
        for syms in sym_groups:
            syms.align_to(heads, LEFT)
            for sym in syms:
                sym.rotate(sym_rot_angle, UP)
            dots.next_to(syms, IN, buff=0.5)
            dots.match_style(syms[0])
            syms.add(dots.copy())

        up_shift = 0.75 * UP
        self.play(
            LaggedStartMap(FadeIn, wq_syms, shift=0.2 * UP, lag_ratio=0.25),
            frame.animate.reorient(59, -7, 0, (-1.62, 0.25, 1.29), 14.18),
            run_time=2,
        )
        for n in range(1, len(sym_groups)):
            self.play(
                LaggedStartMap(FadeIn, sym_groups[n], shift=0.2 * UP, lag_ratio=0.1),
                sym_groups[:n].animate.shift(up_shift),
                run_time=1,
            )
        self.wait()

        # Count up 96 heads
        depth = heads.get_depth()
        brace = Brace(Line(LEFT, RIGHT).set_width(0.5 * depth), UP).scale(2)
        brace_label = brace.get_text("96", font_size=96, buff=MED_SMALL_BUFF)
        brace_group = VGroup(brace, brace_label)
        brace_group.rotate(PI / 2, UP)
        brace_group.next_to(heads, UP, buff=MED_LARGE_BUFF)

        self.add(brace, brace_label, sym_groups)
        self.play(
            frame.animate.reorient(62, -6, 0, (-0.92, -0.08, -0.51), 14.18).set_anim_args(run_time=5),
            GrowFromCenter(brace),
            sym_groups.animate.set_fill(opacity=0.5).set_stroke(width=0),
            FadeIn(brace_label, 0.5 * UP, time_span=(0.5, 1.5)),
        )

        # Set up pure attention patterns, flattened
        for head in heads:
            n_rows = 8
            grid = Square().get_grid(n_rows, 1, buff=0).get_grid(1, n_rows, buff=0)
            grid.set_stroke(WHITE, 1, 0.5)
            grid.set_height(0.9 * head.get_height())
            grid.move_to(head)

            pattern = np.random.normal(0, 1, (n_rows, n_rows))
            for n in range(len(pattern[0])):
                pattern[:, n][n + 1:] = -np.inf
                pattern[:, n] = softmax(pattern[:, n])
            pattern = pattern.T

            dots = VGroup()
            for col, values in zip(grid, pattern):
                for square, value in zip(col, values):
                    if value < 1e-3:
                        continue
                    dot = Dot(radius=0.4 * square.get_height() * value)
                    dot.move_to(square)
                    dots.add(dot)
            dots.set_fill(GREY_B, 1)
            grid.add(dots)

            head.add(grid)
            head.target = head.generate_target()
            grid.set_opacity(0)
            head.target[1].set_opacity(0)
            head.target[0].set_opacity(1)

        n_shown = 4
        heads_target = Group(h.target for h in heads)
        heads_target.arrange(LEFT, buff=MED_LARGE_BUFF)
        heads_target.set_height(1.5)
        heads_target.to_edge(LEFT)
        heads_target.shift(2 * UP)
        heads_target[:-n_shown].set_opacity(0)

        # Set up key/query targets
        for group in sym_groups:
            group.generate_target()
        group_targets = [group.target for group in sym_groups]

        for head, wq, wk, wv_down, wv_up in zip(heads_target[::-1], *group_targets):
            for sym in [wq, wk, wv_down, wv_up]:
                sym.set_fill(opacity=1)
                sym.set_height(0.35)
                sym.rotate(-sym_rot_angle, UP)
            wk.next_to(head, UP, aligned_edge=LEFT)
            wq.next_to(wk, RIGHT, buff=0.35)
            wv_up.next_to(head, UP, aligned_edge=LEFT)
            wv_down.next_to(wv_up, RIGHT, buff=0.35)

        for group in group_targets:
            group[n_shown:].set_opacity(0)

        # Animate the flattening
        right_dots = Tex(R"\dots", font_size=96)
        right_dots.move_to(heads_target[-n_shown - 1], LEFT).shift(MED_SMALL_BUFF * RIGHT)

        brace_group.target = brace_group.generate_target()
        brace_group.target.shift(UP)
        brace_group.target.set_opacity(0)

        self.play(
            frame.animate.reorient(0, 0, 0, ORIGIN, FRAME_HEIGHT).set_anim_args(run_time=2),
            FadeOut(multiple_title, UP),
            MoveToTarget(brace_group, remover=True),
            MoveToTarget(wq_syms, time_span=(0.5, 2)),
            MoveToTarget(wk_syms, time_span=(0.5, 2)),
            FadeOut(wv_down_syms),
            FadeOut(wv_up_syms),
            LaggedStartMap(MoveToTarget, heads, lag_ratio=0.01),
            Write(right_dots, time_span=(1.5, 2.0)),
        )

        att_patterns = VGroup(
            VGroup(head[0], head[2])
            for head in heads[:len(heads) - n_shown - 1:-1]
        )
        self.remove(heads)
        self.add(att_patterns)

        # Show value maps
        for group in [wv_up_syms, wv_down_syms]:
            group.become(group.target)

        value_diagrams = VGroup()
        arrows = VGroup()
        all_v_stacks = VGroup()
        for pattern, wv_up, wv_down, idx in zip(att_patterns, wv_up_syms, wv_down_syms, it.count(1)):
            rect = pattern[0].copy()

            v_stack = VGroup(Tex(Rf"\vec{{\textbf{{v}}}}_{n}") for n in range(1, 4))
            v_stack.arrange(DOWN, buff=LARGE_BUFF)
            v_stack.set_color(RED)
            plusses = VGroup()
            coefs = VGroup()
            for n, v_term in enumerate(v_stack):
                coef = Tex(f"w_{n + 1}")
                coef.next_to(v_term, LEFT, SMALL_BUFF)
                coef.set_fill(GREY_B)
                plus = Tex("+")
                plus.next_to(VGroup(coef, v_term), DOWN)
                plusses.add(plus)
                coefs.add(coef)
            dots = Tex(R"\vdots")
            dots.next_to(plusses, DOWN)
            v_stack.add(coefs, plusses, dots)

            v_stacks = v_stack.replicate(4)
            v_stacks.arrange(RIGHT, buff=LARGE_BUFF)
            v_stacks.set_height(rect.get_height() * 0.85)
            v_stacks.set_fill(border_width=1)

            globals().update(locals())
            v_terms = VGroup(
                *(Tex(Rf"\vec{{\textbf{{v}}}}_{n}^{{({idx})}}") for n in range(1, 4)),
                Tex(R"\dots")
            )
            v_terms[:3].set_color(RED)
            v_terms.arrange(RIGHT)
            v_terms.set_width(0.8 * rect.get_width())
            v_terms.move_to(rect)

            diagram = VGroup(rect, v_terms)
            diagram.to_edge(DOWN, buff=1.5)

            v_stacks.move_to(rect)
            all_v_stacks.add(v_stacks)

            VGroup(wv_up, wv_down).next_to(diagram, UP, buff=SMALL_BUFF, aligned_edge=LEFT)

            arrow = Arrow(pattern, diagram, buff=0.5)
            arrow.shift(0.25 * UP)

            value_diagrams.add(diagram)
            arrows.add(arrow)

        right_dots2 = right_dots.copy()

        self.play(
            LaggedStart(
                (FadeTransform(m1.copy(), m2)
                 for m1, m2 in zip(att_patterns, value_diagrams)),
                lag_ratio=0.25,
                group_type=Group,
            ),
            LaggedStartMap(FadeIn, wv_up_syms, shift=DOWN, lag_ratio=0.25),
            LaggedStartMap(FadeIn, wv_down_syms, shift=DOWN, lag_ratio=0.25),
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.25),
            right_dots2.animate.match_y(value_diagrams).set_anim_args(time_span=(1.0, 1.75)),
        )
        self.wait()

        self.play(
            LaggedStart(
                (Transform(VGroup(diagram[1]), v_stacks)
                 for diagram, v_stacks in zip(value_diagrams, all_v_stacks)),
                lag_ratio=0.25,
                run_time=2
            )
        )
        self.remove(value_diagrams)
        new_diagrams = VGroup(
            VGroup(vd[0], stacks)
            for vd, stacks in zip(value_diagrams, all_v_stacks)
        )
        value_diagrams = new_diagrams
        self.add(value_diagrams)

        # Show sums
        index = 2
        rects = VGroup()
        delta_Es = VGroup()
        arrows = VGroup()
        for n, diagram in enumerate(value_diagrams, start=1):
            diagram.target = diagram.generate_target()
            stacks = diagram.target[1]
            stacks.set_opacity(0.5)
            stacks[index].set_opacity(1)
            rect = SurroundingRectangle(stacks[index], buff=0.05)

            arrow = Vector(0.5 * DOWN)
            arrow.set_color(BLUE)
            arrow.next_to(rect, DOWN, SMALL_BUFF)

            delta_E = Tex(Rf"\Delta \vec{{\textbf{{E}}}}^{{({n})}}_i", font_size=36)
            delta_E.set_color(BLUE)
            delta_E.next_to(arrow, DOWN, SMALL_BUFF)

            rects.add(rect)
            arrows.add(arrow)
            delta_Es.add(delta_E)

        rects.set_stroke(BLUE, 2)

        self.play(
            LaggedStartMap(MoveToTarget, value_diagrams),
            LaggedStartMap(ShowCreation, rects),
            LaggedStartMap(GrowArrow, arrows),
            LaggedStartMap(FadeIn, delta_Es, shift=0.5 * DOWN),
        )
        self.wait()

        # Add together all changes
        low_delta_Es = delta_Es.copy()
        low_delta_Es.scale(1.5)
        low_delta_Es.arrange(RIGHT, buff=0.75)
        low_delta_Es.next_to(delta_Es, DOWN, buff=1.0)
        plusses = VGroup(
            Tex("+", font_size=72).next_to(ldE, buff=0.1).shift(0.1 * DOWN)
            for ldE in low_delta_Es
        )
        dots = Tex(R"\dots", font_size=72).next_to(plusses, RIGHT)

        self.play(
            TransformFromCopy(delta_Es, low_delta_Es),
            Write(plusses),
            Write(dots),
            frame.animate.reorient(0, 0, 0, (-0.99, -1.51, 0.0), 10.71),
        )
        self.wait()

        # Include original embedding
        og_emb = Tex(R"\vec{\textbf{E}}_i", font_size=72)
        og_emb_plus = Tex("+", font_size=72)
        og_emb_plus.next_to(low_delta_Es, LEFT, SMALL_BUFF)
        og_emb.next_to(og_emb_plus, LEFT, 2 * SMALL_BUFF)
        lil_rect = SurroundingRectangle(og_emb)
        big_rect = SurroundingRectangle(VGroup(og_emb, low_delta_Es, dots), buff=0.25)
        lil_rect.set_stroke(WHITE, 2)
        big_rect.set_stroke(TEAL, 3)
        og_label = Text("Original\nembedding")
        new_label = Text("New\nembedding")
        new_label.set_color(TEAL)
        for label in [og_label, new_label]:
            label.next_to(lil_rect, LEFT, buff=MED_LARGE_BUFF)

        self.play(
            FadeIn(og_emb, shift=RIGHT, scale=0.5),
            Write(og_emb_plus),
            FadeIn(og_label, shift=RIGHT),
        )
        self.play(ShowCreation(lil_rect))
        self.wait()
        self.play(
            ReplacementTransform(lil_rect, big_rect),
            FadeTransform(og_label, new_label)
        )
        self.wait()
