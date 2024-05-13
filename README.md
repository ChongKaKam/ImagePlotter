# ImagePlotter

如果你想要将多个图合并在一起，但是因为图片太多，PS或者PPT操作繁琐而苦恼，不妨看看这个小工具。

这是一个基于 Python 的图像排版的工具，并支持英文文字显示。

目前还是一个很简单的工具。计划后续添加更丰富灵活的设置，以及 web 端开发。（画饼）

## 如何使用？
**环境要求**：
+ Pillow
+ matplot

**简单教程**

```python
from ImagePlotter import Box, Text, Canvas

# 初始化画布
canvas = Canvas()
# 为画布添加元素，这里分别添加一个存放图片的 Box 以及一个说明的 Text
image_width  = 32
image_height = 32
image = Box(image_width, image_height, img='path/to/img')

text_width = 32
text_height = 24
text_font = 'path/to/font.ttf'
text_font_size = 18
text_content = 'demo'
text = Text(text_width, text_height, text=f'{text_content}', font_size=text_font_size)

# 绑定到 Canvas 中
image_pos_x, image_pos_y = 0, 0
text_pos_x, text_pos_y = 0, image_pos_y + image_height
canvas.add_component(image_pos_x, image_pos_y, image)
canvas.add_conponent(text_pos_x, text_pos_y, text)

# 在调用 render 之前，程序不会读取任何图片，只是记录下组件的位置信息，
# 在调用 render 之后，canvas 会根据所有组件的位置和大小自动计算画布的宽度和高度，并递归调用组件的 .render() 函数。在这个过程中才会涉及到图片的处理。
# 参数：show - 是否直接显示出来，在服务器上（无显示器）无法查看，因此默认为 False
save_path = 'path/to/save'
canvas.render(save_dir=save_path, save_name=f"demo.png", show=False)
```