class Data:
    '''
    Simple class to store data from xml node
    '''
    def __init__(self, data, css_id, iterable= None, element_name=None) -> None:
        self.data = data
        self.id = css_id
                
        self.iterable = iterable
        self.element_name = element_name
