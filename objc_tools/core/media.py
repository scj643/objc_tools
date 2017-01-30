from ctypes import Structure, c_int32, c_int64, CDLL, c_void_p, c_ulong, c_uint32, c_float
from objc_util import c


kCMTimeFlags_Valid = 1<<0
kCMTimeFlags_HasBeenRounded = 1<<1
kCMTimeFlags_PositiveInfinity = 1<<2
kCMTimeFlags_NegativeInfinity = 1<<3
kCMTimeFlags_Indefinite = 1<<4
kCMTimeFlags_ImpliedValueFlagsMask = kCMTimeFlags_PositiveInfinity | kCMTimeFlags_NegativeInfinity | kCMTimeFlags_Indefinite

class CMTime (Structure):
    '''A Handler for CMTime Structures
    CMTimeValue / CMTimeScale = secomds
    '''
    _fields_ = [('CMTimeValue', c_int64),
                ('CMTimeScale', c_int32),
                ('CMTimeFlags', c_uint32),
                ('CMTimeEpoch', c_ulong)]
    
    @property
    def seconds(self):
        return self.CMTimeValue / self.CMTimeScale
        
    @seconds.setter
    def seconds(self, time):
        self.CMTimeValue = time * self.CMTimeScale


    def __repr__(self):
        return '<CMTime value: {tvalue}, Scale: {tscale}>'.format(tvalue=self.CMTimeValue, tscale=self.CMTimeScale)
                
CMTimeMakeWithSeconds = c.CMTimeMakeWithSeconds
CMTimeMakeWithSeconds.restype = CMTime
CMTimeMakeWithSeconds.argtypes = [c_float, c_int32]

def objc_CMTime(struct):
    '''Converts the AnonymousStructure fromn the returns of some objc functions'''
    return CMTime(struct.a, struct.b, struct.c, struct.d)
