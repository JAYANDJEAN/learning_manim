from utils import *


class SD(Diffusion):
    def __init__(self):
        super().__init__()

    def sd3(self):

        self.prompt.scale(0.6).move_to(5 * LEFT + 2 * UP)

        self.add(self.prompt)




    def construct(self):
        self.camera.background_color = "#1C1C1C"
        self.sd3()



if __name__ == "__main__":
    SD().render()
