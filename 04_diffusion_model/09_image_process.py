import numpy as np
from PIL import Image


def get_noise_image():
    beta_1 = 0.0001
    beta_T = 0.02
    T = 1000
    betas = np.linspace(beta_1, beta_T, T)
    alphas = 1 - betas
    alphas_bar = np.cumprod(alphas)
    sqrt_alphas_bar = np.sqrt(alphas_bar)
    sqrt_one_minus_alphas_bar = np.sqrt(1 - alphas_bar)

    img = Image.open('assets/cat_0.jpg').convert('RGB')
    img = np.array(img) / 255.0
    t_list = list(range(0, 100, 5)) + [999]
    for t in t_list:
        epsilon = np.random.randn(*img.shape)
        x_t = sqrt_alphas_bar[t] * img + sqrt_one_minus_alphas_bar[t] * epsilon
        img_t = (x_t * 255).astype(np.uint8)
        img_t = Image.fromarray(img_t)
        img_t.save(f'assets/cat_0_{t:04}.png')


def get_rgb_image():
    img = Image.open('assets/prompt.png')
    r, g, b = img.split()
    fill = 0
    red = Image.merge('RGB', (r, Image.new("L", r.size, fill), Image.new("L", r.size, fill)))
    green = Image.merge('RGB', (Image.new("L", r.size, fill), g, Image.new("L", r.size, fill)))
    blue = Image.merge('RGB', (Image.new("L", r.size, fill), Image.new("L", r.size, fill), b))
    red.save('assets/prompt_r.png')
    green.save('assets/prompt_g.png')
    blue.save('assets/prompt_b.png')


get_noise_image()
