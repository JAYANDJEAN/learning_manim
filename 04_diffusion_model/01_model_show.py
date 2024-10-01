from clip import CLIP
from ddpm import DDPM
from latent import LATENT
from sd3 import SD3


class Models(DDPM, CLIP, LATENT, SD3):
    def __init__(self):
        super().__init__()

    def construct(self):
        self.camera.background_color = "#1C1C1C"
        self.ddpm1()
        self.ddpm2()
        self.ddpm3()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        self.latent1()
        self.latent2()
        self.sd3()


if __name__ == "__main__":
    Models().render()
