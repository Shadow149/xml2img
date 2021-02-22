class Element:
    def __init__(self, element, data, _id, children, parent):
        self.element = element
        self.data = data
        self.id = _id
        self.children = children
        self.parent = parent

    def __repr__(self):
        if self.element == "Section":
            return f"Section C:{len(self.children)}: E: {self.element} D: {self.data} ID: {self.id} P:{self.parent}"
        return f"{self.children}: E: {self.element} D: {self.data} ID: {self.id} P:{self.parent}"