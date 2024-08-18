from manim import *


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


# Render the scene
if __name__ == "__main__":
    scene = MultipleCuboids()
    scene.render()
