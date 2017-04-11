from objc_util import Structure, c_float, c, c_bool
from pprint import pformat
from objc_util import type_encodings
from objc_tools.structs import Encodings


class Vector3 (Structure):
    _fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]
    type_encoding = 'SCNVector3'
    def __eq__(self, other):
        SCNVector3EqualToVector3 = c.SCNVector3EqualToVector3
        SCNVector3EqualToVector3.argtypes = [Vector3, Vector3]
        SCNVector3EqualToVector3.restype = c_bool
        return SCNVector3EqualToVector3(self, other)
    
    def __repr__(self):
        return '<Vector3: <x: {}, y: {}, z: {}>>'.format(self.x, self.y, self.z)
    
    
class Vector4 (Structure):
    _fields_ = [('x', c_float), ('y', c_float), ('z', c_float), ('w', c_float)]
    type_encoding = 'SCNVector4'
    def __eq__(self, other):
        SCNVector4EqualToVector4 = c.SCNVector4EqualToVector4
        SCNVector4EqualToVector4.argtypes = [Vector4, Vector4]
        SCNVector4EqualToVector4.restype = c_bool
        return SCNVector4EqualToVector4(self, other)       
        
    def __repr__(self):
        return '<Vector3: <x: {}, y: {}, z: {}, w: {}>>'.format(self.x, self.y, self.z, self.w)


class Matrix4 (Structure):
    _fields_ = [('m1_1', c_float), ('m1_2', c_float), ('m1_3', c_float), ('m1_4', c_float),
                ('m2_1', c_float), ('m2_2', c_float), ('m2_3', c_float), ('m2_4', c_float),
                ('m3_1', c_float), ('m3_2', c_float), ('m3_3', c_float), ('m3_4', c_float),
                ('m4_1', c_float), ('m4_2', c_float), ('m4_3', c_float), ('m4_4', c_float)]
    type_encoding = 'SCNMatrix4'
    def matrix_list(self):
        return [[self.m1_1, self.m1_2, self.m1_3, self.m1_4],
                [self.m2_1, self.m2_2, self.m2_3, self.m2_4],
                [self.m3_1, self.m3_2, self.m3_3, self.m3_4],
                [self.m4_1, self.m4_2, self.m4_3, self.m4_4]]
    
    def rotate(self, angle, x, y, z):
        '''rotate
        '''
        self.old = matrix_from_list(self.matrix_list())
        SCNMatrix4Rotate = c.SCNMatrix4Rotate
        SCNMatrix4Rotate.argtypes = [Matrix4, c_float, c_float, c_float, c_float]
        SCNMatrix4Rotate.restype = Matrix4
        return SCNMatrix4Rotate(self, angle, x, y, z)
        
    def scale(self, x, y, z, keep = True):
        '''scale
        :keep: Normally the function replaces the object itself use keep to avoid this
        '''
        self.old = matrix_from_list(self.matrix_list())
        SCNMatrix4Scale = c.SCNMatrix4Scale
        SCNMatrix4Scale.argtypes = [Matrix4, c_float, c_float, c_float]
        SCNMatrix4Scale.restype = Matrix4
        if keep:
            self = self.old
        return SCNMatrix4Scale(self, x, y, z)
        
    def invert(self):
        SCNMatrix4Invert = c.SCNMatrix4Invert
        SCNMatrix4Invert.argtypes = [Matrix4]
        SCNMatrix4Invert.restype = Matrix4
        return SCNMatrix4Invert(self)
        
    def translate(self, tx, ty, tz):
        new = matrix_from_list(self.matrix_list())
        new.m4_1 += tx
        new.m4_2 += ty
        new.m4_3 += tz
        return new
        
    def scale(self, sx, sy, sz):
        new = matrix_from_list(self.matrix_list())
        new.m1_1 += sx
        new.m2_2 += sy
        new.m3_3 += sz
        return new
        
    def rotate (self, angle, x, y, z):
        '''rotate
        Returns a matrix/4 that rotates by an angle in radians about the vector x, y, z'''
        c.SCNMatrix4MakeRotation
        c.SCNMatrix4MakeRotation.argtypes = [Matrix4, c_float, c_float, c_float, c_float]
        c.SCNMatrix4MakeRotation.restype = Matrix4
        return c.SCNMatrix4MakeRotation(self, angle, x, y, z)
        
    def is_identity(self):
        SCNMatrix4IsIdentity = c.SCNMatrix4IsIdentity
        SCNMatrix4IsIdentity.argtypes = [Matrix4]
        SCNMatrix4IsIdentity.restype = c_bool
        return SCNMatrix4IsIdentity(self)
        
    def __mul__(self, other):
        SCNMatrix4Mult = c.SCNMatrix4Mult
        SCNMatrix4Mult.argtypes = [Matrix4, Matrix4]
        SCNMatrix4Mult.restype = Matrix4
        if isinstance(other, (Matrix4)):
            return SCNMatrix4Mult(self, other)
            
    def __eq__(self, other):
        SCNMatrix4EqualToMatrix4 = c.SCNMatrix4EqualToMatrix4
        SCNMatrix4EqualToMatrix4.argtypes = [Matrix4, Matrix4]
        SCNMatrix4EqualToMatrix4.restype = c_bool
        return SCNMatrix4EqualToMatrix4(self, other)
        
    def __repr__(self):
        return '<Matrix4: <Matrix:\n{}>>'.format(pformat(self.matrix_list()))
        

def matrix_from_list(matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]):
    if len(matrix) != 4:
        raise ValueError("Must be a 4x4 list matrix")
    args = []
    for i in matrix:
        if len(i) != 4:
            raise ValueError("Must be a 4x4 list matrix")
        args += i
    return Matrix4(*args)
    

e = Encodings(type_encodings)
for i in [Vector3, Vector4, Matrix4]:
    e.add_structure(i)

e.update_encodings()


