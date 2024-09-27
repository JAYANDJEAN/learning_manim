import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F


def get_pool_image():
    img = Image.open('assets/cat.jpg')
    img = img.convert('RGB')  # 转换为 RGB 格式
    img_np = np.array(img)  # 将PIL图像转换为NumPy数组
    img_tensor = torch.tensor(img_np).permute(2, 0, 1).unsqueeze(0).float()  # 转换为形状 [1, 3, H, W]
    pool_size = (16, 16)
    pooled_img_tensor = F.avg_pool2d(img_tensor, kernel_size=pool_size)
    pooled_img_np = pooled_img_tensor.squeeze(0).permute(1, 2, 0).byte().numpy()
    pooled_img = Image.fromarray(pooled_img_np)
    pooled_img.save('assets/cat_blurred.jpg')


def get_noise_image():
    beta_1 = 0.0001
    beta_T = 0.02
    T = 1000
    betas = np.linspace(beta_1, beta_T, T)
    alphas = 1 - betas
    alphas_bar = np.cumprod(alphas)
    sqrt_alphas_bar = np.sqrt(alphas_bar)
    sqrt_one_minus_alphas_bar = np.sqrt(1 - alphas_bar)

    for i in range(1, 5):
        img = Image.open(f'cats/cat_{i}_000.jpg').convert('RGB')
        img = np.array(img) / 255.0
        t_list = list(range(30, 160, 30))
        for t in t_list:
            epsilon = np.random.randn(*img.shape)
            x_t = sqrt_alphas_bar[t] * img + sqrt_one_minus_alphas_bar[t] * epsilon
            img_t = (x_t * 255).astype(np.uint8)
            img_t = Image.fromarray(img_t)
            img_t.save(f'cats/cat_{i}_{t:03}.jpg')


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


if __name__ == "__main__":
    get_noise_image()
