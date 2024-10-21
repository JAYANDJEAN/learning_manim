# learning_manim

## 01_reflection

1. 改进一些

## 02_transformer

1. 将 manimlib 版本翻译成 manimCE 版本。
   1. https://github.com/3b1b/videos/tree/master/_2024/transformers

## 03_diffusion

1. 需要补充

## 04_protein

1. manim 的 OpenGLSurface 是靠 uv_func 来定义曲面，所以无法实现无规则曲面的渲染。
   1. https://www.reddit.com/r/manim/comments/1fb9wme/how_to_plot_3d_surface_from_xyz_points/
   2. 我理解丝带图也是无规则曲面吧，所以现在不好实现。
   3. 要实现的话，要基于更底层的接口吧，比如 OpenGLMobject。不知道理解是否正确。
2. 如果想要学习丝带图的数据是如何计算的，可以参考：
   1. https://github.com/molstar/molstar/blob/b4772e0cb9c3b3b17290813f97df6766fb0d9876/src/mol-model-props/computed/secondary-structure/dssp.ts

### Videos