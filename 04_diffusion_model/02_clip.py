from PIL import Image

from utils import *


class CLIP(Diffusion):
    def __init__(self):
        super().__init__()

    def clip1(self):
        # 7. show part
        # 还有model_clip
        self.play(FadeTransform(self.title_ddpm, self.title_clip))
        text_encoder = VGroup(self.gear.copy().scale(0.4).set_color(BLUE_C),
                              Text("Text Encoder").scale(0.7)).arrange(RIGHT, buff=0.5)
        image_encoder = VGroup(self.gear.copy().scale(0.4).set_color(BLUE_E),
                               Text("Image Encoder").scale(0.7)).arrange(RIGHT, buff=0.5)
        encoders = VGroup(text_encoder, image_encoder).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        brace_clip = Brace(encoders, direction=LEFT, buff=0.5)
        VGroup(self.model_clip, brace_clip, encoders).arrange(RIGHT, buff=0.7)

        self.play(GrowFromCenter(self.model_clip))
        self.play(GrowFromCenter(brace_clip))
        self.play(
            Indicate(self.model_clip[0][0]),
            TransformFromCopy(self.model_clip[0][0], text_encoder, path_arc=30 * DEGREES)
        )
        self.play(
            Indicate(self.model_clip[0][1]),
            TransformFromCopy(self.model_clip[0][1], image_encoder, path_arc=-30 * DEGREES)
        )
        self.play(FadeOut(brace_clip, encoders))
        self.play(self.model_clip.animate.move_to(2 * LEFT))

        self.wait()

    def clip2(self):
        # 8. clip demo show 3D vector
        # 清理干净
        input_pos = 5 * LEFT
        output_pos = 0.5 * RIGHT
        last_pos = 5 * RIGHT + 1.3 * UP

        text_cat = Text("A CAT").scale(0.9)
        surrounding_text_cat = SurroundingRectangle(
            text_cat, buff=0.1, color=WHITE, corner_radius=0.1, stroke_width=0.7)
        text_cat = VGroup(text_cat, surrounding_text_cat).move_to(input_pos)  #
        embedding_text_cat = WeightMatrix(length=14).set(width=0.5).move_to(output_pos)  #
        brace_text = VGroup(
            Brace(embedding_text_cat, RIGHT, color=GREY),
            Text("768-dimensional").scale(0.5).set_color(YELLOW_E).next_to(embedding_text_cat, RIGHT, 0.6)
        )
        embedding_text_cat.generate_target()
        embedding_text_cat.target.set(width=0.4).move_to(last_pos)  #
        text_cat.generate_target()
        text_cat.target.set(width=0.45).next_to(embedding_text_cat.target, 1.5 * UP)

        image_cat = ImageMobject("assets/cat.jpg").set(height=2).move_to(input_pos)
        embedding_image_cat = WeightMatrix(length=14).set(width=0.5).move_to(output_pos)
        embedding_image_cat.generate_target()
        embedding_image_cat.target.set(width=0.4).move_to(last_pos + 0.6 * LEFT)
        image_cat.generate_target()
        image_cat.target.set(width=0.45).next_to(embedding_image_cat.target, UP)

        text_dog = Text("A DOG").scale(0.9)
        surrounding_text_dog = SurroundingRectangle(
            text_dog, buff=0.1, color=WHITE, corner_radius=0.1, stroke_width=0.7)
        text_dog = VGroup(text_dog, surrounding_text_dog).move_to(input_pos)
        embedding_text_dog = WeightMatrix(length=14).set(width=0.5).move_to(output_pos)
        embedding_text_dog.generate_target()
        embedding_text_dog.target.set(width=0.4).move_to(last_pos + 1.2 * LEFT)
        text_dog.generate_target()
        text_dog.target.set(width=0.45).next_to(embedding_text_dog.target, 1.5 * UP)

        image_dog = ImageMobject("assets/dog.jpg").set(height=2).move_to(input_pos)
        embedding_image_dog = WeightMatrix(length=14).set(width=0.5).move_to(output_pos)
        embedding_image_dog.generate_target()
        embedding_image_dog.target.set(width=0.4).move_to(last_pos + 1.8 * LEFT)
        image_dog.generate_target()
        image_dog.target.set(width=0.45).next_to(embedding_image_dog.target, UP)

        self.play(Create(text_cat))
        self.play(
            AnimationGroup(
                Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                       about_point=self.gears_clip[i].get_center())
                for i in range(2)
            ),
            LaggedStart(bake_mobject_into_vector_entries(text_cat, embedding_text_cat)),
            run_time=3
        )
        self.play(GrowFromCenter(brace_text))
        self.play(FadeOut(brace_text))
        self.play(MoveToTarget(embedding_text_cat), MoveToTarget(text_cat))

        self.play(FadeIn(image_cat))
        self.play(
            AnimationGroup(
                Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                       about_point=self.gears_clip[i].get_center())
                for i in range(2)
            ),
            LaggedStart(bake_mobject_into_vector_entries(image_cat, embedding_image_cat, path_arc=-30 * DEGREES)),
            run_time=3
        )
        self.play(GrowFromCenter(brace_text))
        self.play(FadeOut(brace_text))
        self.play(MoveToTarget(embedding_image_cat), MoveToTarget(image_cat))

        self.play(Create(text_dog))
        self.play(
            AnimationGroup(
                Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                       about_point=self.gears_clip[i].get_center())
                for i in range(2)
            ),
            LaggedStart(bake_mobject_into_vector_entries(text_dog, embedding_text_dog)), run_time=3
        )
        self.play(MoveToTarget(embedding_text_dog), MoveToTarget(text_dog))

        self.play(FadeIn(image_dog))
        self.play(
            AnimationGroup(
                Rotate(self.gears_clip[i], axis=IN if i == 0 else OUT,
                       about_point=self.gears_clip[i].get_center())
                for i in range(2)
            ),
            LaggedStart(bake_mobject_into_vector_entries(image_dog, embedding_image_dog, path_arc=-30 * DEGREES)),
            run_time=3
        )
        self.play(MoveToTarget(embedding_image_dog), MoveToTarget(image_dog))
        self.wait()

        # 9. 3D show
        axes = ThreeDAxes()
        arrow_text_dog = ArrowWithLabel(
            axes.get_origin(),
            [3, 2, 2],
            stroke_width=2.0,
            stroke_color=BLUE,
            label=Text('dog text', font_size=14),
            buff=0,
        )
        arrow_image_dog = ArrowWithLabel(
            axes.get_origin(),
            [1, 3, 1.8],
            stroke_width=2.0,
            stroke_color=BLUE,
            label=Text('dog image', font_size=14),
            buff=0,
        )

        arrow_text_cat = ArrowWithLabel(
            axes.get_origin(),
            [-2, -1, 2],
            stroke_width=2.0,
            stroke_color=RED,
            label=Text('cat text', font_size=14),
            buff=0,
        )
        arrow_image_cat = ArrowWithLabel(
            axes.get_origin(),
            [-1.5, -2, 2.5],
            stroke_width=2.0,
            stroke_color=RED,
            label=Text('cat image', font_size=14),
            buff=0,
        )

        self.play(FadeOut(self.model_clip))
        self.add_fixed_in_frame_mobjects(
            embedding_image_dog, image_dog,
            embedding_text_dog, text_dog,
            embedding_image_cat, image_cat,
            embedding_text_cat, text_cat, self.title_clip
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes))
        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(
            FadeTransform(embedding_image_dog, arrow_image_dog),
            FadeOut(image_dog),
            FadeIn(arrow_image_dog.label)
        )
        self.play(
            FadeTransform(VGroup(embedding_text_dog, text_dog), arrow_text_dog),
            FadeIn(arrow_text_dog.label)
        )
        self.play(
            FadeTransform(embedding_image_cat, arrow_image_cat),
            FadeOut(image_cat),
            FadeIn(arrow_image_cat.label)
        )
        self.play(
            FadeTransform(VGroup(embedding_text_cat, text_cat), arrow_text_cat),
            FadeIn(arrow_text_cat.label)
        )
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(arrow_image_cat, arrow_text_cat,
                          arrow_image_dog, arrow_text_dog,
                          arrow_text_cat.label, arrow_text_dog.label,
                          arrow_image_dog.label, arrow_image_cat.label
                          ))
        self.play(FadeOut(axes))
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        self.wait()

    def clip3(self):
        # 10. show text encoder
        # 只剩model_clip
        phrase = "a cyberpunk with natural greys and whites and browns"
        words = list(filter(lambda s: s.strip(), phrase.split(" ")))
        text_words = VGroup(*[Text(word).scale(0.4) for word in words])
        text_words.arrange(RIGHT, buff=0.15).move_to(RIGHT + 3 * UP)
        rect_words = VGroup()
        for word in text_words:
            rect = SurroundingRectangle(word, buff=-0.013).set_stroke(GREY, 2).set_fill(GREY, 0.2)
            rect.stretch_to_fit_height(0.45)
            rect.stretch_to_fit_width(rect.width + 0.16)
            rect.align_to(word, RIGHT)
            rect_words.add(rect)
        rect_words.set_submobject_colors_by_gradient(BLUE_C, BLUE_D, GREEN)

        text_numbers = VGroup(*[Text(f"{n}", font="Menlo").scale(0.4).next_to(rect_words[i], DOWN, buff=1.0)
                                for i, n in enumerate([4, 14323, 237, 673, 554, 28, 489, 28, 1921])])
        arrow_numbers = VGroup(*[Arrow(rect_words[i].get_bottom(), text_numbers[i].get_top())
                                 for i in range(len(rect_words))])
        brace_numbers = VGroup(
            Brace(VGroup(text_words, text_numbers), LEFT, color=GREY),
            Text("Tokenizer").scale(0.6).set_color(YELLOW_E).next_to(VGroup(text_words, text_numbers), LEFT, 0.7)
        )
        embedding_words = VGroup(*[WeightMatrix(length=10).set(width=0.5).next_to(rect, DOWN, buff=2.0)
                                   for rect in rect_words])
        arrow_embeds = VGroup(*[Arrow(text_numbers[i].get_bottom(), embedding_words[i].get_top())
                                for i in range(len(rect_words))])

        emb_syms = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}").scale(0.9).next_to(rect, DOWN, buff=0.75).set_color(GREY_A)
                            for n, rect in enumerate(rect_words, start=1)])
        arrow_embeds.target = arrow_embeds.generate_target()
        for rect, arrow, sym in zip(rect_words, arrow_embeds.target, emb_syms):
            low_point = sym.get_top()
            top_point = np.array([low_point[0], rect.get_y(DOWN), 0])
            arrow.become(Arrow(top_point, low_point, buff=SMALL_BUFF))

        box_width = emb_syms.get_right()[0] - emb_syms.get_left()[0] + 1

        box = (Rectangle(width=box_width, height=2.0)
               .set_fill(GREY_E, 1).set_stroke(WHITE, 1).move_to(emb_syms.get_center() + 2 * DOWN))
        text_box = Text("Self-Attention").scale(0.7).move_to(box.get_top() + 0.3 * DOWN)
        attention_box = VGroup(box, text_box)
        box_arrows_in = VGroup(*[Arrow(sym.get_bottom(), np.array([sym.get_bottom()[0], box.get_top()[1], 0]))
                                 for sym in emb_syms])
        emb_syms_copy = emb_syms.copy().move_to(box.get_center() + DOWN)
        emb_sym_primes = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}^{{'}}").scale(0.9).move_to(sym.get_center() + 4 * DOWN)
                                  for n, sym in enumerate(emb_syms, start=1)])
        box_arrows_out = VGroup(*[Arrow(np.array([sym.get_bottom()[0], box.get_bottom()[1], 0]),
                                        np.array([sym.get_bottom()[0], emb_sym_primes[i].get_top()[1], 0]))
                                  for i, sym in enumerate(emb_syms)])
        emb_sym_out = emb_sym_primes[-1].copy()
        rect_out = SurroundingRectangle(emb_sym_out).set_stroke(YELLOW_E, 2)
        emb_sym_out.generate_target()
        emb_sym_out.target.scale(1.4).move_to(np.array([text_words.get_center()[0], -0.5, 0]))
        arrow_embed_out = Arrow(text_words.get_bottom() + 0.5 * DOWN, emb_sym_out.target.get_top() + 0.5 * UP)
        embedding_out = WeightMatrix(length=14).set(width=0.5).move_to(emb_sym_out.target)
        arrow_embed_out.generate_target()
        arrow_embed_out.target = Arrow(text_words.get_bottom(), embedding_out.get_top())
        brace_text = VGroup(
            Brace(embedding_out, RIGHT, color=GREY),
            Text("768-dimensional").scale(0.5).set_color(YELLOW_E).next_to(embedding_out, RIGHT, 0.6)
        )
        self.model_clip.move_to(5 * LEFT)

        self.play(GrowFromCenter(self.model_clip))
        self.play(LaggedStartMap(FadeIn, text_words, shift=0.5 * UP, lag_ratio=0.25))
        self.play(LaggedStartMap(DrawBorderThenFill, rect_words))
        self.play(
            LaggedStartMap(GrowArrow, arrow_numbers),
            LaggedStartMap(Create, text_numbers)
        )
        self.play(GrowFromCenter(brace_numbers))
        self.play(
            LaggedStartMap(GrowArrow, arrow_embeds),
            LaggedStartMap(FadeIn, embedding_words, shift=0.5 * DOWN)
        )
        self.play(
            FadeOut(arrow_numbers, text_numbers, brace_numbers),
            LaggedStart(*[Transform(embed, sym)
                          for sym, embed in zip(emb_syms, embedding_words)],
                        group_type=Group,
                        run_time=2
                        ),
            LaggedStartMap(FadeIn, emb_syms, shift=UP),
            MoveToTarget(arrow_embeds, lag_ratio=0.1, run_time=2)
        )
        self.play(
            LaggedStartMap(GrowArrow, box_arrows_in),
            Create(attention_box)
        )
        self.play(
            LaggedStart(
                AnimationGroup(
                    *[ContextAnimation(target, emb_syms_copy,
                                       time_width=2, max_stroke_width=5, lag_ratio=0.2, path_arc=70 * DEGREES)
                      for target in emb_syms_copy])
            ), lag_ratio=0.2
        )
        self.play(
            LaggedStartMap(GrowArrow, box_arrows_out),
            LaggedStartMap(FadeIn, emb_sym_primes, shift=DOWN)
        )
        self.play(Create(rect_out))
        self.play(
            FadeOut(attention_box, box_arrows_in, box_arrows_out, emb_sym_primes,
                    emb_syms, arrow_embeds, rect_out, embedding_words),
            MoveToTarget(emb_sym_out),
            GrowArrow(arrow_embed_out))
        self.play(
            Transform(emb_sym_out, embedding_out),
            MoveToTarget(arrow_embed_out)
        )
        self.play(GrowFromCenter(brace_text))
        self.play(FadeOut(brace_text))
        self.play(FadeOut(emb_sym_out, arrow_embed_out, text_words, rect_words))

        self.wait()

    def clip4(self):
        # 11. show image encoder
        # 只剩model_clip
        image_prompt = Image.open("assets/prompt.png")
        img_width, img_height = image_prompt.size
        num_width, num_height = 3, 3
        sub_images = []
        sub_width = img_width // num_width
        sub_height = img_height // num_height
        for i in range(num_height):
            for j in range(num_width):
                left = j * sub_width
                upper = i * sub_height
                right = (j + 1) * sub_width
                lower = (i + 1) * sub_height
                sub_image = image_prompt.crop((left, upper, right, lower))
                sub_images.append(sub_image)

        image_grid = Group(*[
            Group(*[ImageMobject(np.array(sub_images[num_height * i + j])).scale(0.5)
                    for j in range(num_width)]).arrange(RIGHT, buff=0.0)
            for i in range(num_height)
        ]).arrange(DOWN, buff=0.0)
        image_grid.generate_target()
        image_grid.target = Group(*[
            Group(*[ImageMobject(np.array(sub_images[num_height * i + j])).scale(0.5)
                    for j in range(num_width)]).arrange(RIGHT, buff=0.12)
            for i in range(num_height)
        ]).arrange(DOWN, buff=0.12)

        self.play(FadeIn(image_grid))
        self.play(MoveToTarget(image_grid))
        self.wait()

        image_grid.generate_target()
        image_grid.target = Group(*[
            Group(*[ImageMobject(np.array(sub_images[num_height * i + j])).scale(0.5)
                    for j in range(num_width)]).arrange(RIGHT, buff=0.12)
            for i in range(num_height)
        ]).arrange(RIGHT, buff=0.12).move_to(3 * UP + RIGHT).scale(0.7)
        self.play(MoveToTarget(image_grid))
        self.wait()

        image_grid = Group(*[j for image_grid_line in image_grid for j in image_grid_line])
        image_embedding_words = VGroup(*[WeightMatrix(length=10).set(width=0.5).next_to(im, DOWN, buff=1.0)
                                         for im in image_grid])
        image_arrow_embeds = VGroup(*[Arrow(image_grid[i].get_bottom(), image_embedding_words[i].get_top())
                                      for i in range(len(image_grid))])

        image_emb_syms = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}").scale(0.9)
                                .next_to(im, DOWN, buff=0.75).set_color(GREY_A)
                                  for n, im in enumerate(image_grid, start=1)])
        image_arrow_embeds.generate_target()
        for i, arrow in enumerate(image_arrow_embeds.target):
            arrow.become(Arrow(image_grid[i].get_bottom(), image_emb_syms[i].get_top(), buff=SMALL_BUFF))
        box_width = image_emb_syms.get_right()[0] - image_emb_syms.get_left()[0] + 1

        box = (Rectangle(width=box_width, height=2.0)
               .set_fill(GREY_E, 1).set_stroke(WHITE, 1).move_to(image_emb_syms.get_center() + 2 * DOWN))
        text_box = Text("Self-Attention").scale(0.7).move_to(box.get_top() + 0.3 * DOWN)
        attention_box = VGroup(box, text_box)
        box_arrows_in = VGroup(*[Arrow(sym.get_bottom(), np.array([sym.get_bottom()[0], box.get_top()[1], 0]))
                                 for sym in image_emb_syms])
        emb_syms_copy = image_emb_syms.copy().move_to(box.get_center() + DOWN)
        emb_sym_primes = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}^{{'}}").scale(0.9).move_to(sym.get_center() + 4 * DOWN)
                                  for n, sym in enumerate(image_emb_syms, start=1)])
        box_arrows_out = VGroup(*[Arrow(np.array([sym.get_bottom()[0], box.get_bottom()[1], 0]),
                                        np.array([sym.get_bottom()[0], emb_sym_primes[i].get_top()[1], 0]))
                                  for i, sym in enumerate(image_emb_syms)])
        emb_sym_out = emb_sym_primes[-1].copy()
        rect_out = SurroundingRectangle(emb_sym_out).set_stroke(YELLOW_E, 2)
        emb_sym_out.generate_target()
        emb_sym_out.target.scale(1.4).move_to(np.array([image_grid.get_center()[0], -0.5, 0]))
        arrow_embed_out = Arrow(image_grid.get_bottom() + 0.5 * DOWN, emb_sym_out.target.get_top() + 0.5 * UP)
        embedding_out = WeightMatrix(length=14).set(width=0.5).move_to(emb_sym_out.target)
        arrow_embed_out.generate_target()
        arrow_embed_out.target = Arrow(image_grid.get_bottom(), embedding_out.get_top())

        self.play(
            LaggedStartMap(GrowArrow, image_arrow_embeds),
            LaggedStartMap(FadeIn, image_embedding_words, shift=0.5 * DOWN)
        )
        self.play(
            LaggedStart(*[Transform(embed, sym)
                          for sym, embed in zip(image_emb_syms, image_embedding_words)],
                        group_type=Group,
                        run_time=2
                        ),
            LaggedStartMap(FadeIn, image_emb_syms, shift=UP),
            MoveToTarget(image_arrow_embeds, lag_ratio=0.1, run_time=2)
        )
        self.play(
            LaggedStartMap(GrowArrow, box_arrows_in),
            Create(attention_box)
        )
        self.play(
            LaggedStart(
                AnimationGroup(
                    *[ContextAnimation(target, emb_syms_copy,
                                       time_width=2, max_stroke_width=5, lag_ratio=0.2, path_arc=70 * DEGREES)
                      for target in emb_syms_copy])
            ), lag_ratio=0.2
        )
        self.play(
            LaggedStartMap(GrowArrow, box_arrows_out),
            LaggedStartMap(FadeIn, emb_sym_primes, shift=DOWN)
        )
        self.play(Create(rect_out))
        self.play(
            FadeOut(attention_box, box_arrows_in, box_arrows_out, emb_sym_primes,
                    image_emb_syms, image_arrow_embeds, rect_out, image_embedding_words),
            MoveToTarget(emb_sym_out),
            GrowArrow(arrow_embed_out)
        )
        self.play(
            Transform(emb_sym_out, embedding_out),
            MoveToTarget(arrow_embed_out)
        )
        self.play(FadeOut(emb_sym_out, arrow_embed_out, image_grid))
        self.wait()

    def clip5(self):
        # 12. explain how CLIP works
        self.model_text_encoder.move_to(2.5 * LEFT + 2.5 * UP)
        self.model_image_encoder.move_to(2.5 * LEFT + 1.5 * DOWN)

        text_set = Group(
            Text("A CAT").set(width=2).set_opacity(1.0),
            Text("A CAT").set(width=2).set_opacity(0.4).shift(0.1 * UP + 0.1 * RIGHT),
            Text("A CAT").set(width=2).set_opacity(0.3).shift(0.2 * UP + 0.2 * RIGHT),
            Text("A CAT").set(width=2).set_opacity(0.2).shift(0.3 * UP + 0.3 * RIGHT),
            Text("A CAT").set(width=2).set_opacity(0.1).shift(0.4 * UP + 0.4 * RIGHT),
            Text("A CAT").set(width=2).set_opacity(0.05).shift(0.5 * UP + 0.5 * RIGHT),
        ).move_to(5.5 * LEFT + 2.5 * UP)

        image_set = Group(
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(1.0),
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(0.4).shift(0.1 * UP + 0.1 * RIGHT),
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(0.3).shift(0.2 * UP + 0.2 * RIGHT),
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(0.2).shift(0.3 * UP + 0.3 * RIGHT),
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(0.1).shift(0.4 * UP + 0.4 * RIGHT),
            ImageMobject("assets/cat.jpg").set(width=2).set_opacity(0.05).shift(0.5 * UP + 0.5 * RIGHT),
        ).move_to(5.5 * LEFT + 1.5 * DOWN)

        # lines
        table_mid = 3.5 * RIGHT + 1.5 * DOWN
        grid_size = 0.75
        grid_num = 6
        table = Rectangle(
            width=grid_size * grid_num,
            height=grid_size * grid_num,
            grid_xstep=grid_size,
            grid_ystep=grid_size,
        ).set_stroke(width=2.0, color=GREY).move_to(table_mid)
        table_text = Rectangle(
            width=grid_size * grid_num,
            height=grid_size,
            grid_xstep=grid_size,
        ).set_stroke(width=2.0, color=GREY).next_to(table, UP, buff=0.3)
        table_image = Rectangle(
            width=grid_size,
            height=grid_size * grid_num,
            grid_ystep=grid_size,
        ).set_stroke(width=2.0, color=GREY).next_to(table, LEFT, buff=0.3)
        lines_out_image = VGroup(*[
            CubicBezier(
                self.model_image_encoder.get_right(),
                self.model_image_encoder.get_right() + 1.0 * RIGHT,
                table_image.get_left() + (2.5 * UP + i * DOWN) * grid_size + 1.0 * LEFT,
                table_image.get_left() + (2.5 * UP + i * DOWN) * grid_size,
                stroke_width=2.0
            ) for i in range(grid_num)])
        lines_out_image.set_submobject_colors_by_gradient(TEAL, BLUE_E)

        lines_out_text = VGroup(*[
            CubicBezier(
                self.model_text_encoder.get_right(),
                table_text.get_top() + (2.5 * LEFT + i * RIGHT) * grid_size + 0.7 * UP,
                table_text.get_top() + (2.5 * LEFT + i * RIGHT) * grid_size + 0.6 * UP,
                table_text.get_top() + (2.5 * LEFT + i * RIGHT) * grid_size,
                stroke_width=2.0
            ) for i in range(grid_num)])
        lines_out_text.set_submobject_colors_by_gradient(TEAL, BLUE_E)

        syms_text = VGroup(
            *[MathTex(f"T_{{{i}}}")
              .set(width=grid_size - 0.45)
              .set_color(GREY)
              .move_to(table_text.get_center() + (3.5 * LEFT + i * RIGHT) * grid_size)
              for i in range(1, grid_num + 1)]
        )

        syms_image = VGroup(
            *[MathTex(f"I_{{{i}}}")
              .set(width=grid_size - 0.45)
              .set_color(GREY)
              .move_to(table_image.get_center() + (3.5 * UP + i * DOWN) * grid_size)
              for i in range(1, grid_num + 1)]
        )

        syms_image_text = VGroup(
            *[MathTex(f"I_{{{i}}}", f"\cdot ", f"T_{{{j}}}")
              .set(width=grid_size - 0.2)
              .set_color(GREY)
              .move_to(table_mid + (3.5 * UP + i * DOWN + 3.5 * LEFT + j * RIGHT) * grid_size)
              for j in range(1, grid_num + 1) for i in range(1, grid_num + 1)]
        )

        circle_image_text = VGroup(
            *[Circle(
                radius=random.uniform(0.15, 0.25) if j == i else random.uniform(0.05, 0.1),
                fill_color=GREY, fill_opacity=0.8, stroke_width=0.0
            ).move_to(table_mid + (2.5 * UP + i * DOWN + 2.5 * LEFT + j * RIGHT) * grid_size)
              for j in range(grid_num) for i in range(grid_num)]
        )

        loss_func = MathTex(
            r"\operatorname{loss}=",
            r"-\frac{1}{2|\mathcal{B}|} ",
            r"\sum_{i=1}^{|\mathcal{B}|}\left(",
            r"\log \frac{e^{t \mathbf{x}_i \cdot \mathbf{y}_i}}{\sum_{j=1}^{|\mathcal{B}|} e^{t \mathbf{x}_i \cdot \mathbf{y}_j}}",
            r"+",
            r"\log \frac{e^{t \mathbf{x}_i \cdot \mathbf{y}_i}}{\sum_{j=1}^{|\mathcal{B}|} e^{t \mathbf{x}_j \cdot \mathbf{y}_i}}",
            r"\right)"
        )
        loss_func.move_to(3.5 * LEFT + 0.5 * UP).scale(0.5)
        loss_func_box1 = SurroundingRectangle(
            loss_func[3], buff=0.05, corner_radius=0.01, stroke_width=2.0, stroke_color=YELLOW_E
        )
        loss_func_box2 = SurroundingRectangle(
            loss_func[5], buff=0.05, corner_radius=0.01, stroke_width=2.0, stroke_color=YELLOW_E
        )
        table_box1 = SurroundingRectangle(
            table_text.copy().move_to(table.get_top() + grid_size / 2 * DOWN),
            buff=0.1, corner_radius=0.1, stroke_width=2.0, stroke_color=YELLOW_E
        )
        table_box2 = SurroundingRectangle(
            table_image.copy().move_to(table.get_left() + grid_size / 2 * RIGHT),
            buff=0.1, corner_radius=0.1, stroke_width=2.0, stroke_color=YELLOW_E
        )
        arrow_1 = Arrow(
            table_box1.get_top(), loss_func_box1.get_top(),
            path_arc=30 * DEGREES, buff=0.1,
            stroke_width=2.5, tip_length=0.15,
            max_tip_length_to_length_ratio=1.0,
            max_stroke_width_to_length_ratio=20
        )
        arrow_2 = Arrow(
            table_box2.get_left(), loss_func_box2.get_bottom(),
            path_arc=-30 * DEGREES, buff=0.1,
            stroke_width=2.5, tip_length=0.15,
            max_tip_length_to_length_ratio=1.0,
            max_stroke_width_to_length_ratio=20
        )

        self.play(
            Indicate(self.model_clip[0][0]),
            TransformFromCopy(self.model_clip[0][0], self.model_text_encoder, path_arc=30 * DEGREES)
        )
        self.play(
            Indicate(self.model_clip[0][1]),
            TransformFromCopy(self.model_clip[0][1], self.model_image_encoder, path_arc=-30 * DEGREES)
        )
        self.play(FadeOut(self.model_clip, shift=LEFT))
        self.play(LaggedStartMap(FadeIn, text_set, shift=DOWN, path_arc=30 * DEGREES, lag_ratio=0.1))
        self.play(LaggedStartMap(FadeIn, image_set, shift=DOWN, path_arc=30 * DEGREES, lag_ratio=0.1))
        self.play(FadeIn(table_text), Create(lines_out_text))
        self.play(
            LaggedStart(*[FadeOut(tx, target_position=sym.get_center(), path_arc=30 * DEGREES)
                          for tx, sym in zip(text_set.copy(), syms_text)],
                        lag_ratio=0.05,
                        run_time=2,
                        remover=True
                        ),
            LaggedStartMap(ShowPassingFlash, lines_out_text.copy().set_color(RED),
                           lag_ratio=5e-3,
                           time_width=0.5,
                           run_time=2
                           ),
            LaggedStartMap(Write, syms_text,
                           lag_ratio=0.1,
                           run_time=3
                           ),
        )
        self.play(FadeIn(table_image), Create(lines_out_image))
        self.play(
            LaggedStart(*[FadeOut(tx, target_position=sym.get_center(), path_arc=30 * DEGREES)
                          for tx, sym in zip(image_set.copy(), syms_image)],
                        lag_ratio=0.05,
                        run_time=2,
                        remover=True
                        ),
            LaggedStartMap(ShowPassingFlash, lines_out_image.copy().set_color(RED),
                           lag_ratio=5e-3,
                           time_width=0.5,
                           run_time=2
                           ),
            LaggedStartMap(Write, syms_image,
                           lag_ratio=0.1,
                           run_time=3
                           ),
        )
        self.play(FadeIn(table))
        self.add(syms_image_text)
        self.play(
            LaggedStart(
                *[LaggedStart(
                    *[TransformFromCopy(syms_text[i], syms_image_text[grid_num * i + j][2], path_arc=30 * DEGREES)
                      for j in range(grid_num)],
                    lag_ratio=0.1
                ) for i in range(grid_num)],
                lag_ratio=0.1,
                run_time=4
            ),
            LaggedStart(
                *[LaggedStart(
                    *[TransformFromCopy(syms_image[i], syms_image_text[grid_num * i + j][0], path_arc=-30 * DEGREES)
                      for j in range(grid_num)],
                    lag_ratio=0.1
                ) for i in range(grid_num)],
                lag_ratio=0.1,
                run_time=4
            ),
        )
        self.play(
            syms_image_text.animate.set_opacity(0.3),
            FadeIn(circle_image_text)
        )
        self.play(Write(loss_func))
        self.play(Create(loss_func_box1), Create(table_box1))
        self.play(GrowArrow(arrow_1))
        self.play(Create(loss_func_box2), Create(table_box2))
        self.play(GrowArrow(arrow_2))
        self.play(FadeOut(loss_func_box1, table_box1, arrow_1, loss_func_box2, table_box2, arrow_2,
                          syms_image_text, table, table_text, syms_text, table_image, syms_image,
                          lines_out_text, lines_out_image, circle_image_text, loss_func, text_set, image_set,
                          self.model_image_encoder, self.model_text_encoder))
        self.wait()

    def clip6(self):
        bert = ImageMobject("assets/bert.png").set(width=2.5).move_to(5 * LEFT)
        text_bert = Text("Does Bert work?").scale(1.1).move_to(2.5 * UP)
        image_cat_glasses = ImageMobject("assets/cat_glasses.jpg").set(width=4.0).next_to(text_bert, DOWN, buff=0.7)
        text_cat_glasses = Text("a cat with glasses").scale(0.5).next_to(image_cat_glasses, DOWN, buff=0.2)
        text_answer = Text("No!").next_to(text_bert, RIGHT, buff=1.0)
        box = SurroundingRectangle(text_cat_glasses[8:],
                                   color=YELLOW_E, buff=0.05, corner_radius=0.05, stroke_width=1.5)

        self.add(bert, text_bert, image_cat_glasses, text_cat_glasses, text_answer, box)

    def construct(self):
        self.camera.background_color = "#1C1C1C"
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        # self.clip6()


if __name__ == "__main__":
    CLIP().render()
