from manim import *


class RoundedRectanglesWithArrow(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Create the first rounded rectangle with text on the left side
        left_rect = RoundedRectangle(corner_radius=0.3, width=2, height=1, color=BLUE, fill_opacity=0.5)
        left_text = Text("Start").move_to(left_rect.get_center())
        left_group = VGroup(left_rect, left_text)  # Group the rectangle and text together
        left_group.to_edge(LEFT, buff=1)  # Move to the left side

        # Create the second rounded rectangle with text in the center
        center_rect = RoundedRectangle(corner_radius=0.3, width=2, height=1, color=GREEN, fill_opacity=0.5)
        center_text = Text("Diffusion Model").move_to(center_rect.get_center())
        center_group = VGroup(center_rect, center_text)  # Group the rectangle and text together
        center_group.move_to(ORIGIN)  # Place in the center of the screen

        # Create an arrow pointing from the left rectangle to the center rectangle
        arrow = Arrow(start=left_group.get_right(), end=center_group.get_left(), buff=0.2, color=BLACK)

        # Animate the creation of the left rectangle with text
        self.play(Create(left_group))
        self.wait(0.5)

        # Animate the creation of the center rectangle with text
        self.play(Create(center_group))
        self.wait(0.5)

        # Animate the creation of the arrow
        self.play(Create(arrow))
        self.wait(1)


# Render the scene
if __name__ == "__main__":
    scene = RoundedRectanglesWithArrow()
    scene.render()
