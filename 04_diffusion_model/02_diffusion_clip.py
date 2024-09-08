from PIL import Image

from utils import *


class CLIP(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        gear = SVGMobject("assets/wheel.svg")
        # CLIP
        text_clip = Text("CLIP", font="menlo").to_edge(UL, buff=0.5).scale(0.7)

        gears_clip = VGroup(gear.copy().scale(0.5).shift(0.8 * UP).rotate(10 * DEGREES).set_color('#3fc1c9'),
                            gear.copy().scale(0.5).shift(0.55 * RIGHT).rotate(-8 * DEGREES).set_color('#364f6b'))
        text_clip_model = Text("CLIP Model", font_size=24, color=GREY).next_to(gears_clip, DOWN, SMALL_BUFF)
        surrounding_clip = SurroundingRectangle(VGroup(gears_clip, text_clip_model),
                                                buff=0.2, color=WHITE, corner_radius=0.3).set_stroke(width=0.5)
        model_clip = VGroup(gears_clip, text_clip_model, surrounding_clip).move_to(ORIGIN)

        text_cat = Text("A CAT").scale(0.9)
        surrounding_text_cat = SurroundingRectangle(
            text_cat, buff=0.1, color=WHITE, corner_radius=0.1).set_stroke(width=0.7)
        text_cat = VGroup(text_cat, surrounding_text_cat).move_to(3 * LEFT)
        embedding_text_cat = WeightMatrix(length=14).set(width=0.5).move_to(2.5 * RIGHT)
        brace_text = Brace(embedding_text_cat, direction=RIGHT, buff=0.1)
        dim_text = Text("768-dimensional", font_size=24).set_color(YELLOW).next_to(brace_text, RIGHT)
        embedding_text_cat.generate_target()
        embedding_text_cat.target.scale(0.7).move_to(6 * RIGHT + 1 * UP)
        text_cat.generate_target()
        text_cat.target.scale(0.3).next_to(embedding_text_cat.target, UP)

        image_cat = ImageMobject("assets/cat_0.jpg").set(height=2).move_to(3 * LEFT)
        embedding_image = WeightMatrix(length=14).set(width=0.5).move_to(2.5 * RIGHT)
        embedding_image.generate_target()
        embedding_image.target.scale(0.7).move_to(5 * RIGHT + 1 * UP)
        image_cat.generate_target()
        image_cat.target.scale(0.15).next_to(embedding_image.target, UP)

        text_dog = Text("A DOG").scale(0.9)
        surrounding_text_dog = SurroundingRectangle(
            text_dog, buff=0.1, color=WHITE, corner_radius=0.1).set_stroke(width=0.7)
        text_dog = VGroup(text_dog, surrounding_text_dog).move_to(3 * LEFT)
        embedding_text_dog = WeightMatrix(length=14).set(width=0.5).move_to(2.5 * RIGHT)
        embedding_text_dog.generate_target()
        embedding_text_dog.target.scale(0.7).move_to(4 * RIGHT + 1 * UP)
        text_dog.generate_target()
        text_dog.target.scale(0.3).next_to(embedding_text_dog.target, UP)

        all_embedding = VGroup(embedding_text_cat, embedding_image, embedding_text_dog)
        all_label = Group(text_cat, image_cat, text_dog)
        all_embedding.generate_target()
        all_embedding.target.set(width=0.5).arrange(LEFT, buff=0.3).move_to(1.3 * LEFT + 0.3 * DOWN)
        all_label.generate_target()
        for i, label in enumerate(all_label.target):
            label.set(width=0.6).next_to(all_embedding.target[i], UP)

        self.add(text_clip)
        self.play(FadeIn(model_clip))
        self.play(Create(text_cat))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(gears_clip[i], axis=IN if i == 0 else OUT, about_point=gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(text_cat, embedding_text_cat))
        )
        self.play(GrowFromCenter(brace_text), Create(dim_text))
        self.play(FadeOut(brace_text, dim_text))
        self.play(MoveToTarget(embedding_text_cat), MoveToTarget(text_cat))

        self.play(FadeIn(image_cat))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(gears_clip[i], axis=IN if i == 0 else OUT, about_point=gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(image_cat, embedding_image, path_arc=-30 * DEGREES))
        )
        self.play(MoveToTarget(embedding_image), MoveToTarget(image_cat))

        self.play(Create(text_dog))
        self.play(
            LaggedStart(
                AnimationGroup(
                    Rotate(gears_clip[i], axis=IN if i == 0 else OUT, about_point=gears_clip[i].get_center())
                    for i in range(2)
                ), run_time=3, lag_ratio=0.0),
            LaggedStart(bake_mobject_into_vector_entries(text_dog, embedding_text_dog)),
        )
        self.play(MoveToTarget(embedding_text_dog), MoveToTarget(text_dog))
        self.wait()
        self.play(model_clip.animate.shift(4 * LEFT + 0.3 * DOWN),
                  MoveToTarget(all_embedding),
                  MoveToTarget(all_label))
        self.wait()
        self.play(FadeOut(all_embedding, all_label, target_position=4 * RIGHT, scale=0.6))
        self.play(model_clip.animate.shift(LEFT))

        # show part
        # text_encoder = VGroup(gear.copy().scale(0.5).set_color('#3fc1c9'),
        #                       Text("Text Encoder", font="menlo").scale(0.7)).arrange(RIGHT, buff=0.5)
        # image_encoder = VGroup(gear.copy().scale(0.5).set_color('#364f6b'),
        #                        Text("Image Encoder", font="menlo").scale(0.7)).arrange(RIGHT, buff=0.5)
        # encoders = VGroup(text_encoder, image_encoder).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        # brace_clip = Brace(encoders, direction=LEFT, buff=0.5)
        # VGroup(brace_clip, encoders).next_to(model_clip, RIGHT)
        #
        # self.play(GrowFromCenter(brace_clip))
        # self.play(
        #     FadeIn(text_encoder, shift=0.5 * UP),
        #     FadeIn(image_encoder, shift=0.5 * DOWN)
        # )
        # self.play(FadeOut(brace_clip, text_encoder, image_encoder))

        # show text encoder
        phrase = "a cyberpunk with natural greys and whites and browns"
        words = list(filter(lambda s: s.strip(), phrase.split(" ")))
        text_words = VGroup(*[Text(word, font="menlo").scale(0.4) for word in words])
        text_words.arrange(RIGHT, buff=0.15).move_to(RIGHT + 3 * UP)
        rect_words = VGroup()
        for word in text_words:
            rect = SurroundingRectangle(word, buff=-0.013).set_stroke(GREY, 2).set_fill(GREY, 0.2)
            rect.stretch_to_fit_height(0.45)
            rect.stretch_to_fit_width(rect.width + 0.16)
            rect.align_to(word, RIGHT)
            rect_words.add(rect)
        rect_words.set_submobject_colors_by_gradient(BLUE_C, BLUE_D, GREEN)

        text_numbers = VGroup(*[Text(f"{n}", font="menlo").scale(0.4).next_to(rect_words[i], DOWN, buff=1.0)
                                for i, n in enumerate([4, 14323, 237, 673, 554, 28, 489, 28, 1921])])
        arrow_numbers = VGroup(*[Arrow(rect_words[i].get_bottom(), text_numbers[i].get_top())
                                 for i in range(len(rect_words))])

        embedding_words = VGroup(*[WeightMatrix(length=10).set(width=0.5).next_to(rect, DOWN, buff=2.0)
                                   for rect in rect_words])
        arrow_embeds = VGroup(*[Arrow(text_numbers[i].get_bottom(), embedding_words[i].get_top())
                                for i in range(len(rect_words))])

        emb_syms = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}").next_to(rect, DOWN, buff=0.75).set_color(GREY_A)
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
        emb_sym_primes = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}^{{'}}").move_to(sym.get_center() + 4 * DOWN)
                                  for n, sym in enumerate(emb_syms, start=1)])
        box_arrows_out = VGroup(*[Arrow(np.array([sym.get_bottom()[0], box.get_bottom()[1], 0]),
                                        np.array([sym.get_bottom()[0], emb_sym_primes[i].get_top()[1], 0]))
                                  for i, sym in enumerate(emb_syms)])
        emb_sym_out = emb_sym_primes[-1].copy()
        rect_out = SurroundingRectangle(emb_sym_out).set_stroke(YELLOW, 2)
        emb_sym_out.generate_target()
        emb_sym_out.target.scale(1.4).move_to(np.array([text_words.get_center()[0], -0.5, 0]))
        arrow_embed_out = Arrow(text_words.get_bottom(), emb_sym_out.target.get_top())
        embedding_out = WeightMatrix(length=14).set(width=0.5).move_to(emb_sym_out.target)
        arrow_embed_out.generate_target()
        arrow_embed_out.target = Arrow(text_words.get_bottom(), embedding_out.get_top())

        self.play(LaggedStartMap(FadeIn, text_words, shift=0.5 * UP, lag_ratio=0.25))
        self.play(LaggedStartMap(DrawBorderThenFill, rect_words))
        self.play(
            LaggedStartMap(GrowArrow, arrow_numbers),
            LaggedStartMap(Create, text_numbers)
        )
        self.play(
            LaggedStartMap(GrowArrow, arrow_embeds),
            LaggedStartMap(FadeIn, embedding_words, shift=0.5 * DOWN)
        )
        self.play(
            FadeOut(arrow_numbers, text_numbers),
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
            MoveToTarget(arrow_embed_out))
        self.wait()

        # show image encoder
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
        self.play(FadeOut(emb_sym_out, arrow_embed_out, text_words, rect_words))
        self.play(FadeIn(image_grid))
        self.play(MoveToTarget(image_grid))
        self.wait()

        image_grid.generate_target()
        image_grid.target = Group(*[
            Group(*[ImageMobject(np.array(sub_images[num_height * i + j])).scale(0.5)
                    for j in range(num_width)]).arrange(RIGHT, buff=0.12)
            for i in range(num_height)
        ]).arrange(RIGHT, buff=0.12).move_to(3 * UP + RIGHT).scale(0.7)
        # image_grid.target = Group(*[ImageMobject(np.array(sub_image)).scale(0.5)
        #                             for sub_image in sub_images]).arrange(RIGHT, buff=0.12).move_to(
        #     3 * UP + RIGHT).scale(0.7)
        self.play(MoveToTarget(image_grid))
        self.wait()

        image_grid = Group(*[ImageMobject(np.array(sub_image)).scale(0.5)
                             for sub_image in sub_images]).arrange(RIGHT, buff=0.12).move_to(
            3 * UP + RIGHT).scale(0.7)
        image_embedding_words = VGroup(*[WeightMatrix(length=10).set(width=0.5).next_to(im, DOWN, buff=1.0)
                                         for im in image_grid])
        image_arrow_embeds = VGroup(*[Arrow(image_grid[i].get_bottom(), image_embedding_words[i].get_top())
                                      for i in range(len(image_grid))])

        image_emb_syms = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}").next_to(im, DOWN, buff=0.75).set_color(GREY_A)
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
        emb_sym_primes = VGroup(*[MathTex(f"\\vec{{E}}_{{{n}}}^{{'}}").move_to(sym.get_center() + 4 * DOWN)
                                  for n, sym in enumerate(image_emb_syms, start=1)])
        box_arrows_out = VGroup(*[Arrow(np.array([sym.get_bottom()[0], box.get_bottom()[1], 0]),
                                        np.array([sym.get_bottom()[0], emb_sym_primes[i].get_top()[1], 0]))
                                  for i, sym in enumerate(image_emb_syms)])
        emb_sym_out = emb_sym_primes[-1].copy()
        rect_out = SurroundingRectangle(emb_sym_out).set_stroke(YELLOW, 2)
        emb_sym_out.generate_target()
        emb_sym_out.target.scale(1.4).move_to(np.array([image_grid.get_center()[0], -0.5, 0]))
        arrow_embed_out = Arrow(image_grid.get_bottom(), emb_sym_out.target.get_top())
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
            GrowArrow(arrow_embed_out))
        self.play(
            Transform(emb_sym_out, embedding_out),
            MoveToTarget(arrow_embed_out))
        self.wait()
        self.play(FadeOut(emb_sym_out, arrow_embed_out, image_grid))
        self.wait(3)




class CLIPEmbedding(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"

        text_cat = Text("A CAT").scale(0.1).move_to(2 * LEFT)
        image_cat = ImageMobject("assets/cat_0.jpg").set(height=0.5).move_to(2.1 * LEFT)
        text_dog = Text("A DOG").scale(0.1).move_to(2 * RIGHT, 2 * UP)
        self.add_fixed_in_frame_mobjects(text_cat, text_dog, image_cat)
        axes = ThreeDAxes()
        vector1 = Arrow3D(start=ORIGIN, end=2 * DOWN + 2 * RIGHT + 4 * UP, color=RED)
        vector2 = Arrow3D(start=ORIGIN, end=2.1 * DOWN + 2.1 * RIGHT + 3 * UP, color=GREEN)
        vector3 = Arrow3D(start=ORIGIN, end=2 * UP + 2 * LEFT + 3 * UP, color=BLUE)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES, focal_distance=20.0)
        self.play(Create(axes))
        self.play(Create(vector1), Write(text_cat))
        self.play(Create(vector2), FadeIn(image_cat))
        self.play(Create(vector3), Write(text_dog))
        # self.begin_ambient_camera_rotation(rate=0.05)  # 以一定速度旋转相机
        # self.stop_ambient_camera_rotation()
        self.wait(2)


if __name__ == "__main__":
    scene = CLIP()
    scene.render()
