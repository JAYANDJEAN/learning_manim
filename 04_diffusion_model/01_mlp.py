import random

from manim import *


class MultiLayerPerceptron(MovingCameraScene):
    def construct(self):
        def create_composed_shape(radius):
            circle = Circle(radius=radius, color=WHITE).set_stroke(width=1.5)
            line1 = Line(circle.get_center(), circle.point_at_angle(PI / 3), color=BLUE_B).set_stroke(width=2)
            line2 = Line(circle.get_center(), circle.point_at_angle(PI), color=BLUE_B).set_stroke(width=2)
            return VGroup(circle, line1, line2)

        def create_connections(nodes_in, nodes_out):
            full_connections = VGroup()
            combinations = [(x, y) for x in range(len(nodes_in)) for y in range(len(nodes_out))]
            random_choices = random.sample(combinations, 5)
            for i, node1 in enumerate(nodes_in):
                for j, node2 in enumerate(nodes_out):
                    if node2.get_color() != ORANGE:
                        line = Line(node1.get_right(), node2.get_left(), buff=SMALL_BUFF)
                        line.set_stroke(GREY_B, width=random.random() ** 2, opacity=random.random() ** 0.25)
                        if (i, j) in random_choices:
                            line.set_stroke(WHITE, width=0.5 + random.random(), opacity=1)
                        full_connections.add(line)
            return full_connections

        self.camera.background_color = "#1C1C1C"
        num_layers = 7
        random_integers = [random.randint(5, 7) for _ in range(num_layers)]
        dict_layer_nodes = dict()
        for i, num_nodes in enumerate(random_integers):
            if i == 0:
                circles = ([Circle(radius=0.2, color=ORANGE).set_stroke(width=1.5)] +
                           [Circle(radius=0.2, color=WHITE).set_stroke(width=1.5) for _ in range(num_nodes)])
            elif i == len(random_integers) - 1:
                circles = [Circle(radius=0.2, color=WHITE).set_stroke(width=1.5) for _ in range(num_nodes)]
            else:
                circles = ([Circle(radius=0.2, color=ORANGE).set_stroke(width=1.5)] +
                           [create_composed_shape(0.2) for _ in range(num_nodes)])
            dict_layer_nodes[i] = VGroup(*circles).arrange(UP, buff=0.3)

        node01 = VGroup(dict_layer_nodes[0], dict_layer_nodes[1]).arrange(RIGHT, buff=3)
        connections01 = create_connections(dict_layer_nodes[0], dict_layer_nodes[1])
        brace_in = Brace(node01[0], direction=LEFT)
        brace_in_text = Text("Input", font_size=24, color=YELLOW).next_to(brace_in, LEFT, SMALL_BUFF)
        brace_out = Brace(node01[1], direction=RIGHT)
        brace_out_text = Text("Output", font_size=24, color=YELLOW).next_to(brace_out, RIGHT, SMALL_BUFF)
        brace_01 = Brace(node01, direction=UP)
        brace_01_text = Text("Parameters", font_size=24, color=YELLOW).next_to(brace_01, UP, SMALL_BUFF)
        node01_copy = node01.copy()
        nodes = VGroup(*dict_layer_nodes.values()).arrange(RIGHT, buff=1.3)
        connections = VGroup(*[create_connections(dict_layer_nodes[i], dict_layer_nodes[i + 1])
                               for i in range(num_layers - 1)])
        brace_mlp = Brace(nodes, direction=UP)
        brace_mlp_text = Text("MultiLayerPerceptron", font_size=24, color=YELLOW).next_to(brace_mlp, UP, SMALL_BUFF)

        self.play(Create(node01_copy[0]))
        self.play(Create(brace_in))
        self.play(Create(brace_in_text))
        self.play(Create(node01_copy[1]))
        self.play(Create(brace_out))
        self.play(Create(brace_out_text))
        self.play(Create(connections01))
        self.play(Create(brace_01))
        self.play(Create(brace_01_text))
        self.play(FadeOut(brace_in, brace_in_text, brace_out, brace_out_text, brace_01, brace_01_text),
                  FadeOut(connections01))

        self.wait()
        self.play(Transform(node01_copy, nodes))
        self.wait()
        self.play(Create(connections))
        self.play(Create(brace_mlp), Create(brace_mlp_text))


if __name__ == "__main__":
    scene = MultiLayerPerceptron()
    scene.render()
