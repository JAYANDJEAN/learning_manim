from manim import *


class TextBoxInputAnimation(Scene):
    def construct(self):
        # 创建一个文本框矩形
        text_box = Rectangle(width=6, height=1, color=WHITE, fill_opacity=0.1)
        text_box.to_edge(UP)

        # 创建一个初始为空的文本对象
        input_text = Text("", font_size=36)
        input_text.next_to(text_box, DOWN)

        # 将文本框和初始文本添加到场景中
        self.add(text_box, input_text)

        # 模拟输入的内容
        input_string = "Hello, Manim!"

        # 创建一个动画效果逐字显示文本
        for char in input_string:
            # 更新文本内容
            new_text = Text(input_text.text + char, font_size=36)
            new_text.next_to(text_box, DOWN)
            # 使用 Transform 替换旧文本
            self.play(Transform(input_text, new_text), run_time=0.3)

        # 保持最终场景
        self.wait()


if __name__ == "__main__":
    scene = TextBoxInputAnimation()
    scene.render()
