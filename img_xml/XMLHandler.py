from parsel import Selector
from .Element import Element
from .ImageElement import ImageElement
import time

class XMLHandler:
    def __init__(self, path, constants):
        self.xml = open(path,'r').read()
        self.xml_list = []
        self.constants = constants

    def _get_nodes(self,nodes, parent_element):
        for node in nodes:
            if len(node.xpath("child::*")) == 0:
                element = node.get().split(' ')[0][1:]
                css_id = node.xpath("@id").getall()
                data = node.xpath("@text|@src").getall()

                n = Element(element, data, css_id, [], parent_element)
                ie = ImageElement(n, self.constants)
                if parent_element != None:
                    parent_element.element.children.append(ie)
                else:
                    self.xml_list.append(ie)
            else: 
                css_id = node.xpath("@id").getall()
                n = Element("Section",None,css_id,[],parent_element)
                ie = ImageElement(n, self.constants)
                self._get_nodes(node.xpath("child::*"),ie)
                if parent_element != None:
                    parent_element.element.children.append(ie)
                else:
                    self.xml_list.append(ie)

    def get_xml_elements(self):
        start = time.time()
        selector = Selector(text=self.xml)
        nodes = selector.xpath("//root/*")
        self._get_nodes(nodes, None)
        print(f"XMLHandler: {time.time() - start}s")
        return self.xml_list
