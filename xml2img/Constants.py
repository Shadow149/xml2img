class Constants:
    def __init__(self, margin = 50, 
                       header_family = "fonts/reaver-black.otf", 
                       header_size = 40, 
                       font_family = "fonts/radiance-bold.otf", 
                       font_size = 24, 
                       text_colour = [255,255,255]):
        self.default_margin = margin

        self.header_font_family = header_family
        self.header_font_size = header_size

        self.default_font_family = font_family
        self.default_font_size = font_size

        self.default_colour = text_colour
    
    def set_default_margin(self, foo):
        self.default_margin = foo
    
    def set_header_font_family(self, foo):
        self.header_font_family = foo
    
    def set_header_font_size(self, foo):
        self.header_font_size = foo
    
    def set_default_font_family(self, foo):
        self.default_font_family = foo
    
    def set_default_font_size(self, foo):
        self.default_font_size = foo
    
    def set_default_colour(self, foo):
        self.default_colour = foo
    
    
    
    
