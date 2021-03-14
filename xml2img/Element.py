from .Data import Data

class Element:
    
    SECTION = 'Section'
    
    REPEATED_SECTION = 'RepeatedSection'
    
    
    def __init__(self, element, data, _id, children, parent, iterable = None, element_name = None):
        self.element = element
        self.data = Data(data, _id, iterable, element_name)
        
        self.parent = parent
        self.children = children
                
    def __repr__(self):
        if self.element in [Element.SECTION, Element.REPEATED_SECTION]:
            return f"Section C:{len(self.children)}: E: {self.element} D: {self.data} ID: {self.data.id} P:{self.parent} I: {self.data.iterable} {self.data.element_name}"
        return f"{self.children}: E: {self.element} D: {self.data} ID: {self.data.id} P:{self.parent}"