from ctypes import Structure, c_int32, c_int64, CDLL, c_void_p, c_ulong, c_uint32, c_float
from objc_util import c


class CMTime (Structure):
    '''A Handler for CMTime Structures'''
    _fields_ = [('CMTimeValue', c_int64),
                ('CMTimeScale', c_int32),
                ('CMTimeFlags', c_uint32),
                ('CMTimeEpoch', c_ulong)]
                
CMTimeMakeWithSeconds = c.CMTimeMakeWithSeconds
CMTimeMakeWithSeconds.restype = CMTime
CMTimeMakeWithSeconds.argtypes = [c_float, c_int32]

def objc_CMTime(struct):
    '''Converts the AnonymousStructure fromn the returns of some objc functions'''
    return CMTime(struct.a, struct.b, struct.c, struct.d)
