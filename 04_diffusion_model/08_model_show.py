from utils import *


class Models(Diffusion):
    def __init__(self):
        super().__init__()

    def construct(self):
        self.camera.background_color = "#1C1C1C"
        self.add(self.model_diffusion)


if __name__ == "__main__":
    Models().render()
