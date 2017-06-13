__doc__ = """structs: 
             Usage: import objc_util's type_encoding into your script
             Then make an Encodings class passing type_encoding as the param"""
             
from ctypes import Structure


class Encodings (object):
    def __init__(self, encoding_list):
        self.origonal_encodings = encoding_list.copy()
        self.new_encodings = {}
        self.encodings = encoding_list
        
    def add_structure(self, item, encoding_name = None, update = True):
        if issubclass(item, (Structure)):
            if not encoding_name:
                if 'type_encoding' in item.__dict__.keys():
                    encoding_name = item.type_encoding
                else:
                    raise ValueError('No type encoding given')
                name = '{' + encoding_name + '}'
                self.new_encodings[name] = item
                if update:
                    self.update_encodings()
        else:
            raise TypeError('not a Structure type')
            
    @property
    def structures(self):
        returns = {}
        for i in self.encodings.keys():
            if ('{' and '}') in i:
                returns[i] = self.encodings[i]
        return returns
    
    def update_encodings(self):
        for k, v in self.new_encodings.items():
            self.encodings[k] = v
        
if __name__ == '__main__':
    from objc_util import type_encodings
    t=Encodings(type_encodings)
