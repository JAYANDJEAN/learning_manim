from manim import *
import gensim.downloader
import os
import random


def get_word_to_vec_model(model_name="glove-wiki-gigaword-50"):
    filename = f"assets/{model_name}"
    if os.path.exists(filename):
        return gensim.models.keyedvectors.KeyedVectors.load(filename)
    model = gensim.downloader.load(model_name)
    model.save(filename)
    return model


def get_principle_components(data, n_components=3):
    covariance_matrix = np.cov(data, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

    order_of_importance = np.argsort(eigenvalues)[::-1]
    sorted_eigenvectors = eigenvectors[:, order_of_importance]  # sort the columns
    return sorted_eigenvectors[:, :n_components]


class Word2VecScene(ThreeDScene):
    def __init__(self):
        super().__init__()
        axes_config = dict(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-4, 4, 1),
        )
        stroke_width = 1.0
        embedding_model = "glove-wiki-gigaword-50"
        self.model = get_word_to_vec_model(embedding_model)
        self.basis = get_principle_components(self.model.vectors, 3).T
        self.axes = ThreeDAxes(**axes_config)
        self.plane = NumberPlane(
            self.axes.x_range, self.axes.y_range,
            background_line_style=dict(
                stroke_width=stroke_width,
            ),
            faded_line_style=dict(
                stroke_opacity=0.25,
                stroke_width=0.5 * stroke_width,
            ),
            faded_line_ratio=1,
        )

    def get_labeled_vector(
            self,
            word,
            coords=None,
            stroke_width=5,
            color=YELLOW,
            func_name: str | None = "E",
            buff=0.05,
            direction=None,
            label_config: dict = dict()
    ):
        # Return an arrow with word label next to it
        axes = self.axes
        if coords is None:
            coords = self.basis @ self.model[word.lower()]
        point = axes.c2p(*coords)
        return Arrow(
            axes.get_origin(),
            point
        )


# done
class AmbientWordEmbedding(Word2VecScene):
    def __init__(self):
        super().__init__()

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        axes = self.axes
        axes.set_stroke(width=2).set_height(7).move_to(2 * RIGHT + 1.0 * IN)

        # Add titles
        titles = VGroup(Text("Words"), Text("Vectors"))
        colors = [YELLOW, BLUE]
        titles.set_height(0.5)
        xs = [-4.0, axes.get_x()]
        for title, x, color in zip(titles, xs, colors):
            title.move_to(x * RIGHT)
            title.to_edge(UP)
            title.add(Underline(title))
            title.set_color(color)
            self.add_fixed_in_frame_mobjects(title)

        arrow = Arrow(titles[0], titles[1], buff=0.5)
        self.add_fixed_in_frame_mobjects(arrow)

        arrow_label = Text("``Embedding''")
        arrow_label.set_submobject_colors_by_gradient(YELLOW, BLUE)
        arrow_label.next_to(arrow, UP, SMALL_BUFF)
        self.add_fixed_in_frame_mobjects(arrow_label)

        self.add(titles)
        self.add(arrow)

        # Add words
        words = "All data in deep learning must be represented as vectors".split(" ")
        pre_labels = VGroup(*(Text(word) for word in words))
        pre_labels.arrange(DOWN, aligned_edge=LEFT)
        pre_labels.next_to(titles[0], DOWN, buff=0.5)
        pre_labels.align_to(titles[0][0], LEFT)
        pre_labels.set_backstroke(0.1)
        self.add_fixed_in_frame_mobjects(pre_labels)

        coords = np.array([
            self.basis @ self.model[word.lower()]
            for word in words
        ])
        coords -= coords.mean(0)
        max_coord = max(coords.max(), -coords.min())
        coords *= 4.0 / max_coord

        embeddings = VGroup(*(
            self.get_labeled_vector(
                word,
                coord,
                stroke_width=2,
                color=interpolate_color(BLUE_D, BLUE_A, random.random()),
                func_name=None,
                label_config=dict(font_size=24)
            )
            for word, coord in zip(words, coords)
        ))

        self.play(LaggedStartMap(FadeIn, pre_labels, shift=0.2 * UP, lag_ratio=0.1, run_time=1))

        # Transition
        self.add(turn_animation_into_updater(
            Write(arrow_label, time_span=(1, 3))
        ))
        for label, vect in zip(pre_labels, embeddings):
            self.add(turn_animation_into_updater(
                TransformFromCopy(label, vect, run_time=2)
            ))
            self.add(turn_animation_into_updater(
                FadeIn(vect, run_time=1)
            ))
            self.wait(0.5)
        self.play(Create(arrow_label, time_width=1.5, run_time=3))
        self.wait(15)


if __name__ == "__main__":
    scene = AmbientWordEmbedding()
    scene.render()
