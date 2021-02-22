class Element:
    def __init__(self, element, data, _id, children, parent, iterable = None, element_name = None, sectionType = "Section"):
        self.element = element
        self.data = data
        self.id = _id
        self.children = children
        self.parent = parent
        
        self.iterable = iterable
        self.element_name = element_name
        self.sectionType = sectionType

    def __repr__(self):
        if self.element == "Section":
            return f"Section C:{len(self.children)}: E: {self.element} D: {self.data} ID: {self.id} P:{self.parent} I: {self.iterable} {self.element_name}"
        return f"{self.children}: E: {self.element} D: {self.data} ID: {self.id} P:{self.parent}"