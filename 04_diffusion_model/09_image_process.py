import torch
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

    def extract(v, t, x_shape):
        device = t.device
        out = torch.gather(v, index=t, dim=0).float().to(device)
        return out.view([t.shape[0]] + [1] * (len(x_shape) - 1))

    # t = torch.randint(T, size=(1,), device='cpu')
    # noise = torch.randn_like(x_0)
    # # extract 计算第t步加了噪音的图片，noisy_img
    # x_t = (extract(sqrt_alphas_bar, t, x_0.shape) * x_0 +
    #        extract(sqrt_one_minus_alphas_bar, t, x_0.shape) * noise)


def get_rgb_image():
    img = Image.open('assets/prompt.png')
    r, g, b = img.split()
    fill = 0
    # 创建新的图像并填充0（黑色）
    red = Image.merge('RGB', (r, Image.new("L", r.size, fill), Image.new("L", r.size, fill)))
    green = Image.merge('RGB', (Image.new("L", r.size, fill), g, Image.new("L", r.size, fill)))
    blue = Image.merge('RGB', (Image.new("L", r.size, fill), Image.new("L", r.size, fill), b))

    # 保存每个通道到文件
    red.save('assets/red_channel.png')
    green.save('assets/green_channel.png')
    blue.save('assets/blue_channel.png')


get_rgb_image()