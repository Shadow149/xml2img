from img_xml.XMLImage import XMLImage
from img_xml.Constants import Constants

class TestImg (XMLImage):
    def __init__(self, width, height, xml_path, css_path, background_colour, constants):
        super().__init__(width, height, xml_path, css_path, background_colour, constants)

    def initialise_variables(self):
        self.set_variable("test_iterable",[1,2,3,4,5])
        pass

if __name__ == "__main__":
    consts = Constants(text_colour=(0,0,0))
    ti = TestImg(500,700,'layouts/image.xml','styles/style.css', (255, 255, 255), consts)
    ti.initialise_variables()
    ti.create()