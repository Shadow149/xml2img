from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .XMLHandler import XMLHandler
from .CSSHandler import CSSHandler
import requests
import io
import ast

import time

class XMLImage:
    def __init__(self, width, height, xml_path, css_path, background_colour, constants):
        self.width = width
        self.height = height

        self.xml_path = xml_path
        self.css_path = css_path

        self.xml_handler = XMLHandler(xml_path, constants) 
        self.css_handler = CSSHandler(css_path)

        start = time.time()
        self.img = Image.new('RGBA', (width, height), color = background_colour)
        self.text_layer = Image.new('RGBA', (width, height), color = (255,255,255,0))
        self.draw = ImageDraw.Draw(self.text_layer)
        print(f"XMLImage.__init__: {time.time() - start}")
    
    def set_variable(self, attr, value):
        if not hasattr(self, attr):
            self.__setattr__(attr, value)

    def process_css(self, imageElement, rules):
        for id_ in imageElement.element.id:#
            if id_ not in rules:
                continue

            idents = rules[id_]
            for ident in idents:
                value = idents[ident]
                if type(idents[ident]) == str:
                    value = self.eval_string(idents[ident])

                if ident == "display":
                    if value == "inline":
                        imageElement.inline = True
                        imageElement.o_inline = True
                    elif value == "flex":
                        imageElement.background = True
                    else:
                        imageElement.inline = False
                        imageElement.o_inline = False
                elif ident == "margin-left":
                    imageElement.left_margin += int(value)
                elif ident == "margin-right":
                    imageElement.right_margin += int(value)
                elif ident == "margin-bottom":
                    imageElement.bottom_margin += int(value)
                elif ident == "margin-top":
                    imageElement.top_margin += int(value)
                elif ident == "margin":
                    imageElement.left_margin += int(value)
                    imageElement.top_margin += int(value)
                    imageElement.bottom_margin += int(value)
                    imageElement.right_margin += int(value)
                elif ident == "width":
                    imageElement.img_width = int(value)
                elif ident == "height":
                    imageElement.img_height = int(value)
                elif ident == "font-family":
                    imageElement.font_family = value
                elif ident == "font-size":
                    imageElement.font_size = int(value)
                elif ident == "color":
                    c = value
                    # handle variable
                    if type(value) == str:
                        c = ast.literal_eval(value)
                    imageElement.color = list(map(int, c))
                elif ident == "opacity":
                    imageElement.opacity = value

        return imageElement

    def init_elements(self, elements, rules):
        for i in range(len(elements)):
            elements[i] = self.process_css(elements[i],rules)
            if elements[i].element.data != None:
                if len(elements[i].element.data) > 0:
                    elements[i].element.data[0] = self.eval_string(elements[i].element.data[0])
            elements[i].init_vars()
            self.init_elements(elements[i].element.children, rules)
    
    def eval_string(self, non_f_str: str):
        return eval(f'f"""{non_f_str}"""')

    def process(self, elements, rules):

        for imageElement in elements:  
            
            if imageElement.element.element == "Section":
                imageElement.init_pos(self.draw)
                self.process(imageElement.element.children, rules)  

            if imageElement.element.parent == None:
                pass
            
            start = time.time()
            if imageElement.element.element != "Section":
                if imageElement.element.element == "title":
                    text = imageElement.element.data[0]
                    font = ImageFont.truetype(imageElement.font_family, int(imageElement.font_size))
                    self.draw.text((imageElement.x_off,imageElement.y_off), text, font=font, fill=tuple(imageElement.color))

                if imageElement.element.element == "label":
                    text = imageElement.element.data[0]
                    font = ImageFont.truetype(imageElement.font_family, int(imageElement.font_size))
                    self.draw.text((imageElement.x_off,imageElement.y_off), text, font=font, fill=tuple(imageElement.color))
                
                elif imageElement.element.element == "image":
                    if imageElement.img_height != None or imageElement.img_width != None:
                        imageElement.pil_data = self.resize_image(imageElement.pil_data, imageElement.img_height, imageElement.img_width)
                    
                    if imageElement.pil_data == None:
                        return
                        
                    mode = imageElement.pil_data.mode
                    
                    if mode == 'RGBA':
                        self.img.paste(imageElement.pil_data, (int(imageElement.x_off),int(imageElement.y_off)), imageElement.pil_data)
                    else:
                        self.img.paste(imageElement.pil_data, (int(imageElement.x_off),int(imageElement.y_off)))
                
                elif imageElement.element.element == "block":
                    self.draw.rectangle((imageElement.x_off,imageElement.y_off, imageElement.x_off + imageElement.img_width, imageElement.y_off + imageElement.img_height), fill=tuple(imageElement.color))
            print(f"XMLImage.process rendering: {time.time() - start}")

    def resize_image(self, img, new_h, new_w):
        width, height = img.size

        new_h = int(new_w * height / width )
        new_w  = int(new_h * width / height)

        return img.resize((new_w, new_h), Image.ANTIALIAS)

    def create(self):
        elements = self.xml_handler.get_xml_elements()
        rules = self.css_handler.get_css()

        start = time.time()
        self.init_elements(elements, rules)
        print(f"XMLImage.init_elements: {time.time() - start}")
        start = time.time()
        self.process(elements, rules)
        print(f"XMLImage.process: {time.time() - start}")

        start = time.time()
        self.img = Image.alpha_composite(self.img, self.text_layer)
        self.img.save("new_info.png")
        print(f"Image save: {time.time() - start}")
        return self.img
