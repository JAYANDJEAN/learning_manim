from manim import *


class SquareFrontCuboidParallel(ThreeDScene):
    def construct(self):
        # Set up the axes (optional for reference)
        axes = ThreeDAxes()

        # Dimensions for the cuboid
        side_length = 3  # This will be both the width and the height of the front face
        depth = 2  # The depth of the cuboid

        # Create the cuboid (Prism with square front face)
        cuboid = Prism(dimensions=[side_length, side_length, depth], fill_color=BLUE, fill_opacity=0.5)

        # Position the camera so the front face is square and bottom is parallel to the screen
        # self.set_camera_orientation(phi=0 * DEGREES, theta=-10 * DEGREES)

        # Slightly rotate the cuboid to align the bottom edge with the screen
        cuboid.rotate(PI / 2, axis=UP)

        # Add the axes and the cuboid to the scene
        self.add(axes, cuboid)

        # Pause to view the scene
        self.wait()

class MultipleCuboids(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        self.set_camera_orientation(phi=70 * DEGREES, theta=0 * DEGREES, gamma=0 * DEGREES)
        axes = ThreeDAxes()

        cuboids = []
        num_cuboids = 5
        distance_between = 0.5

        for i in range(num_cuboids):
            cuboid = Prism(dimensions=[3, 0.2, 3], fill_color=BLUE_C)
            cuboid.shift(UP * i * distance_between)
            cuboids.append(cuboid)

        cuboid_group = VGroup(*cuboids)
        self.add(axes, cuboid_group)
        self.wait()


class CuboidWithAxes(ThreeDScene):
    def construct(self):
        # Set up the 3D coordinate axes
        axes = ThreeDAxes()

        point = (0, 2, 0)
        prism_original = Prism(dimensions=[4, 1, 4], fill_color=BLUE_C, stroke_width=1)
        prism_rotate = prism_original.rotate(70 * DEGREES, axis=UP, about_point=point)

        # Add the axes, cuboid, and labels to the scene
        self.play(Transform(prism_original, prism_rotate))

        # Pause to view the scene
        self.wait()


class FlowingLines(Scene):
    def construct(self):
        # Define the function for the flowing line
        def func(t):
            return np.array([t, np.sin(2 * t), 0])

        # Create the line using ParametricFunction
        line = ParametricFunction(
            func, t_min=-PI, t_max=PI, color=BLUE, stroke_width=4
        )

        # Create an animation where the line flows
        flowing_line = line.copy().shift(LEFT * 4)

        # Create a moving animation
        self.play(MoveAlongPath(flowing_line, line), run_time=4, rate_func=linear)

        # Pause to view the scene
        self.wait()

# Render the scene
if __name__ == "__main__":
    scene = FlowingLines()
    scene.render()
