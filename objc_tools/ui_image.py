from objc_util import ObjCInstance, c, c_void_p
from ctypes import c_double
from io import BytesIO
from base64 import decodestring

UIImagePNGRepresentation = c.UIImagePNGRepresentation
UIImagePNGRepresentation.restype = c_void_p
UIImagePNGRepresentation.argtypes = [c_void_p]


def png_buffer(img):
    data=ObjCInstance(UIImagePNGRepresentation(img))
    b64 = decodestring(data.base64EncodedString().cString())
    buffer = BytesIO(b64)
    return buffer

def png_rep(img):
    return ObjCInstance(UIImagePNGRepresentation(img))
