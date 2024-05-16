import os
import re
import yaml
import math
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

class Box:
    def __init__(self, width:int=16, height:int=16, margin:list=[0,0,0,0], img=None, rotate=0) -> None:
        self.attrs = {
            'width': width,
            'height': height,
            'margin': margin,    # up,down,left,right
            'img': img,
            'rotate': rotate,
        }
    
    def set(self, attr, value):
        self.attrs[attr] = value

    def get_attr(self, attr):
        return self.attrs[attr]

    def render(self):
        # if canvas == None:
        #     raise ValueError(f'Box: canvas is None: {canvas}')
        if self.attrs['img'] is None:
            raise ValueError(f"this box has invalid img: ({self.attrs['img']})")
        if not os.path.exists(self.attrs['img']):
            raise ValueError(f"invalid img path: {self.attrs['img']}")
        self.image = Image.open(self.attrs['img'])
        # resize
        self.image = self.image.resize((self.attrs['width'], self.attrs['height']), Image.BILINEAR)
        return self.image

class Text:
    def __init__(self, width:int=16, height:int=16, margin:list=[0,0,0,0], 
                 text='', font:str='', font_size:int=24, text_align:str='center') -> None:
        self.attrs = {
            'width': width,
            'height': height,
            'margin': margin,    # up,down,left,right
            'text_align': text_align,
            'font': font,
            'font_size': font_size,
            'text': text,
        }
        if font == '':  # set default font
            font = os.path.join(os.path.dirname(__file__), 'TimesNewRoman.ttf')
        self.font = ImageFont.truetype(font, font_size)
        # print(self.attrs)
    def set(self, attr, value):
        self.attrs[attr] = value

    def get_attr(self, attr):
        return self.attrs[attr]
    
    def render(self):
        self.text_image = Image.new('RGB', (self.attrs['width'], self.attrs['height']), 'white')
        self.draw = ImageDraw.Draw(self.text_image)
        (left, top, right, bottom) = self.font.getbbox(self.attrs['text'])
        text_width = right-left
        text_height = bottom-top
        text_color = (0,0,0)
        pos_x = 0
        pos_y = 0
        # alignment
        if self.attrs['text_align'] == 'center':
            pos_x = (self.attrs['width']-text_width)//2
            pos_y = (self.attrs['height']-text_height)//2
        elif self.attrs['text_align'] == 'left':
            pos_x = 0
            pos_y = (self.attrs['height']-text_height)//2   
        elif self.attrs['text_align'] == 'right':
            pos_x = (self.attrs['width']-text_width)
            pos_y = (self.attrs['height']-text_height)//2
        else:
            raise ValueError(f"unknown alignment: {self.attrs['text_align']}")
        # draw text
        self.draw.text((pos_x, pos_y), self.attrs['text'], font=self.font, fill=text_color)
        # self.text_image = self.text_image.rotate(self.attrs['rotate'],expand=True)
        # self.attrs['width'] = self.text_image.width
        # self.attrs['height'] = self.text_image.height
        return self.text_image

class Canvas:
    def __init__(self) -> None:
        self.total_width  = 0
        self.total_height = 0
        self.background = 'white'
        self.comps = []
        self.layer = None

    def add_component(self, pos_x, pos_y, comp, theta=0):
        new_comp = [pos_x, pos_y, theta, comp]
        theta_radians = theta/180*math.pi
        self.comps.append(new_comp)

        width = comp.get_attr('width')
        height = comp.get_attr('height')
        comp_width = int(width * math.cos(theta_radians) + height * math.sin(theta_radians))
        comp_height = int(height * math.cos(theta_radians) + width * math.sin(theta_radians))

        canvas_width = pos_x + comp_width
        canvas_height = pos_y + comp_height

        # update total_width
        if self.total_width < canvas_width:
            self.total_width = canvas_width
        if self.total_height < canvas_height:
            self.total_height = canvas_height

    def render(self, save_dir='./', save_name='CanvaseRender.png', show=False):
        self.layer = Image.new('RGB', (self.total_width, self.total_height), 'white')
        for pos_x, pos_y, theta, comp in self.comps:
            comp_img = comp.render()
            comp_img = comp_img.rotate(theta, expand=True, fillcolor='white')
            self.layer.paste(comp_img, (pos_x, pos_y))
        # save image
        save_path = os.path.join(save_dir, save_name)
        self.layer.save(save_path)
        # show image?
        if show:
            self.layer.show()

# Test
def test():

    pad = 1
    size = 128
    box1 = Box(size, size, img='../images/celeba/gaussian_deblur/noise_free/ddnm/generated/0_-1.png')
    box2 = Box(size, size, img='../images/celeba/gaussian_deblur/noise_free/ddnm/generated/0_-1.png')
    text = Text(size, 32, text='DDPM', font_size=24, font='/home/zhuangjiaxin/workspace/diffusion/ImagePlotter/TimesNewRoman.ttf')
    # box3 = Box(256, 256, img='../images/celeba/gaussian_deblur/noise_free/ddnm/generated/0_-1.png')
    # box4 = Box(256, 256, img='../images/celeba/gaussian_deblur/noise_free/ddnm/generated/0_-1.png')
    # demo.render()
    # demo.image.save('./demo.png')
    canvas = Canvas()
    canvas.add_component(0,0,box1)
    canvas.add_component(size+pad,0,box2)
    canvas.add_component(0,size+pad,box2)
    canvas.add_component(size+pad,size+pad,box2)
    canvas.add_component(0, 2*size+pad, text)
    # canvas.add_box(0,256+10,box2)
    # canvas.add_box(256+10,256+10,box2)
    canvas.render(save_name='demo.png')

if __name__ == '__main__':
    test()
