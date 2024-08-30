from manimlib import *
import warnings


def softmax(logits, temperature=1.0):
    logits = np.array(logits)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')  # Ignore all warnings within this block
        logits = logits - np.max(logits)  # For numerical stability
        exps = np.exp(np.divide(logits, temperature, where=temperature != 0))

    if np.isinf(exps).any() or np.isnan(exps).any() or temperature == 0:
        result = np.zeros_like(logits)
        result[np.argmax(logits)] = 1
        return result
    return exps / np.sum(exps)


class MultiHeadedAttention(InteractiveScene):
    def construct(self):
        # Mention head
        background_rect = FullScreenRectangle()
        title = Text("Multi-headed attention").scale(1.25).to_edge(UP)
        self.add(background_rect, title)
        self.wait()

        # Set up images
        n_heads = 4
        heads = Group()
        for n in range(n_heads):
            im = ImageMobject("assets/prompt.png").set_opacity(1).shift(0.01 * OUT)
            rect = SurroundingRectangle(im, buff=0.2).set_fill(BLACK, 0.75).set_stroke(WHITE, 1, 1)
            heads.add(Group(rect, im))

        # Show many parallel layers
        self.set_floor_plane("xz")
        frame = self.frame
        title.fix_in_frame()
        background_rect.fix_in_frame()

        heads.set_height(4).arrange(OUT, buff=1.0).move_to(DOWN)

        pre_head = ImageMobject("assets/prompt.png").move_to(4 * LEFT)

        self.add(pre_head)
        self.wait()
        self.play(
            frame.animate.reorient(41, -12, 0, (-1.0, -1.42, 1.09), 12.90).set_anim_args(run_time=2),
            background_rect.animate.set_fill(opacity=0.75),
            FadeTransform(pre_head, heads[-1], time_span=(1, 2)),
        )
        self.play(
            frame.animate.reorient(48, -11, 0, (-1.0, -1.42, 1.09), 12.90),
            LaggedStart((FadeTransform(heads[-1].copy(), image) for image in heads),
                        lag_ratio=0.1,
                        group_type=Group,
                        ),
            run_time=4,
        )
        self.add(heads)
        self.wait()
        self.play(frame.animate.reorient(59, -7, 0, (-1.62, 0.25, 1.29), 14.18), run_time=1)
        self.wait()
        self.play(frame.animate.reorient(62, -6, 0, (-0.92, -0.08, -0.51), 14.18).set_anim_args(run_time=5))

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

        self.play(
            frame.animate.reorient(0, 0, 0, ORIGIN, FRAME_HEIGHT).set_anim_args(run_time=2),
            LaggedStartMap(MoveToTarget, heads, lag_ratio=0.01),
        )
