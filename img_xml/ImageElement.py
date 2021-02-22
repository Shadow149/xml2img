import requests
import ast
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import time

class ImageElement:
    def __init__(self, element, constants):
        self.constants = constants
        
        self.element = element
        self.inline = False
        self.o_inline = False
        self.x_off = self.constants.DEFAULT_MARGIN
        self.y_off = self.constants.DEFAULT_MARGIN

        self.left_margin = 0
        self.right_margin = 0
        self.top_margin = 0
        self.bottom_margin = 0

        self.width, self.height = 0,0

        self.pil_data = None
        self.img_height = None
        self.img_width = None

        self.background = False

        self.font_size = self.constants.DEFAULT_FONT_SIZE
        self.font_family = self.constants.DEFAULT_FONT_FAMILY

        self.color = self.constants.DEFAULT_COLOUR
        self.opacity = 1
    
    def init_size(self, draw):
        size = self.get_size(draw)
        if not self.background:
            self.width = size[0] + self.left_margin - self.right_margin
            self.height = size[1] + self.top_margin - self.bottom_margin
        else:
            self.width, self.height = 0, 0
        return self.width, self.height

    def get_size(self, draw):
        if not (self.width == 0 and self.height == 0):
            return self.width, self.height

        if self.element.element == "Section":
            widths, heights = [], []
            width, height = 0, 0
            for i in range(len(self.element.children)):
                w, h = self.element.children[i].init_size(draw)
                widths.append(w)
                heights.append(h)

                if self.o_inline:
                    width += w
                    height = max(heights)
                else:
                    width = max(widths)
                    height += h

            return width, height

        if self.element.element == "title":
            text = self.element.data[0]

            if self.font_size == self.constants.DEFAULT_FONT_SIZE:
                self.font_size = self.constants.HEADER_FONT_SIZE

            self.font_family = self.constants.HEADER_FONT_FAMILY
            
            font = ImageFont.truetype(self.constants.HEADER_FONT_FAMILY, int(self.font_size))
            text_size = draw.textsize(text, font)
            return text_size[0] + 10, self.font_size + 10

        if self.element.element == "label":
            text = self.element.data[0]
                
            font = ImageFont.truetype(self.font_family, int(self.font_size))
            text_size = draw.textsize(text, font)
            return text_size[0] + 10, self.font_size + 10

        elif self.element.element == "image":
                
            path = self.element.data[0]
            if len(path) == 0:
                img = None
                return 0,0
            elif path[:4] == "http":
                img = Image.open(requests.get(path, stream=True).raw)
            elif path[0] == 'b':
                img = Image.open(io.BytesIO(eval(path)))
            else:
                img = Image.open(path)

            self.pil_data = img
            image_size = img.size
            
            if self.img_height != None or self.img_width != None:
                return self.img_width, self.img_height

            return image_size[0], image_size[1]

        elif self.element.element == "block":
            return self.img_width, self.img_height 

        return 0,0
    
    def init_vars(self):
        if self.element.parent != None:
            self.x_off = self.element.parent.x_off
            self.y_off = self.element.parent.y_off
            self.inline = self.element.parent.o_inline

    def init_pos(self, draw):
        start = time.time()
        x = self.x_off + self.left_margin - self.right_margin
        y = self.y_off + self.top_margin - self.bottom_margin
        for i in range(len(self.element.children)):    
            self.element.children[i].init_vars()
            self.element.children[i].init_size(draw)

            if not self.element.children[i].inline:
                self.element.children[i].y_off = y
                self.y_off = y
                y += self.element.children[i].height 
            else:
                self.element.children[i].x_off = x
                self.x_off = x
                x += self.element.children[i].width
            
            self.element.children[i].x_off += self.element.children[i].left_margin - self.element.children[i].right_margin
            self.element.children[i].y_off += self.element.children[i].top_margin - self.element.children[i].bottom_margin

        print(f"ImageElement.init_pos: {time.time() - start}")
        
        