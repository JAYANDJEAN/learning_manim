# learning_manim

## 01_reflection

1. 圆和椭圆里的光反射。

## 02_transformer

1. 将 manimlib 版本翻译成 manimCE 版本。
   1. https://github.com/3b1b/videos/tree/master/_2024/transformers

## 03_diffusion

1. 需要补充

## 04_protein

1. manim 的 OpenGLSurface 是靠 uv_func 来实现 init_points，所以无法实现无规则曲面的渲染，要实现的话，要基于更底层的接口 OpenGLMobject。
2. 我理解只要新建一个 OpenGLSurfacePoint，继承于 OpenGLMobject，读取输入的 point 来实现 init_points 就可以。
3. 如果想要学习丝带图的数据是如何计算的，可以参考：
   1. https://github.com/molstar/molstar/blob/b4772e0cb9c3b3b17290813f97df6766fb0d9876/src/mol-model-props/computed/secondary-structure/dssp.ts

### Videos