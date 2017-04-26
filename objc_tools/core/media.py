from ctypes import Structure, c_int32, c_int64, c_uint32, c_double
from objc_util import c, type_encodings
from objc_tools.backports.enum_backport import Flag
from objc_tools.structs import Encodings

class CMTimeFlags (Flag):
    Valid = 1<<0
    HasBeenRounded = 1<<1
    PositiveInfinity = 1<<2
    NegativeInfinity = 1<<3
    Indefinite = 1<<4
    ImpliedValueFlagsMask = PositiveInfinity | NegativeInfinity | Indefinite

class CMTime (Structure):
    '''A Handler for CMTime Structures
    DO NOT CALL DIRECTLY use CMTimeMake
    '''
    _fields_ = [('CMTimeValue', c_int64),
                ('CMTimeScale', c_int32),
                ('CMTimeFlags', c_uint32),
                ('CMTimeEpoch', c_int64)]
    type_encoding = 'CMTime'
    @property
    def seconds(self):
        '''Return the object as seconds'''
        try:
            return self.CMTimeValue / self.CMTimeScale
        except ZeroDivisionError:
            return 0
        
    @seconds.setter
    def seconds(self, time):
        self.CMTimeValue = time * self.CMTimeScale
    
    @property
    def flags(self):
        return CMTimeFlags(self.CMTimeFlags)
    
        
    def __repr__(self):
        return '<CMTime value: {tvalue}, scale: {tscale}, seconds: {sec}>'.format(tvalue=self.CMTimeValue, tscale=self.CMTimeScale, sec=self.seconds)
        
    def __add__(self, other):
        return CMTimeAdd(self, other)
        
    def __sub__(self, other):
        return CMTimeSubtract(self, other)
        
    def __mul__(self, other):
        return CMTimeMultiplyByFloat64(self, other)
        
    def __truediv__(self, other):
        return self * (1/other)
        
    def __eq__(self, other):
        if CMTimeCompare(self, other) == 0:
            return True
        else:
            return False
            
    def __lt__(self, other):
        if CMTimeCompare(self, other) == -1:
            return True
        else:
            return False
        
    def __le__(self, other):
        if CMTimeCompare(self, other) <= 0:
            return True
        else:
            return False
    
    def __gt__(self, other):
        if CMTimeCompare(self, other) == 1:
            return True
        else:
            return False
            
    def __ge__(self, other):
        if CMTimeCompare(self, other) >= 0:
            return True
        else:
            return False
    
    def __bool__(self):
        '''Return True if the CMTime is valid'''
        if CMTimeFlags.Valid in self.flags:
            return True
        else:
            return False
        
e = Encodings(type_encodings)
e.add_structure(CMTime)

def CMTimeMake(value, scale = 90000):
    '''Make a CMTime
       :param value: The numerator of the resulting CMTime.
       :param scale: The denomenator of the resulting CMTime.
       :rtype: 
       '''
    CMTimeMake = c.CMTimeMake
    CMTimeMake.argtypes = [c_int64, c_int32]
    CMTimeMake.restype = CMTime
    return CMTimeMake(value, scale)


def CMTimeMakeWithSeconds(seconds, scale = 90000):
    '''Make a CMTime
    :param seconds: Number of seconds
    :param scale: the scale of which seconds goes into
    '''
    CMTimeMakeWithSeconds = c.CMTimeMakeWithSeconds
    CMTimeMakeWithSeconds.argtypes = [c_double, c_int32]
    CMTimeMakeWithSeconds.restype = CMTime
    return CMTimeMakeWithSeconds(seconds, scale)



CMTimeMultiplyByFloat64 = c.CMTimeMultiplyByFloat64
CMTimeMultiplyByFloat64.argtypes = [CMTime, c_double]
CMTimeMultiplyByFloat64.restype = CMTime

CMTimeGetSeconds = c.CMTimeGetSeconds
CMTimeGetSeconds.argtypes = [CMTime]
CMTimeGetSeconds.restype = c_double

CMTimeAdd = c.CMTimeAdd
CMTimeAdd.argtypes = [CMTime, CMTime]
CMTimeAdd.restype = CMTime

CMTimeSubtract = c.CMTimeSubtract
CMTimeSubtract.argtypes = [CMTime, CMTime]
CMTimeSubtract.restype = CMTime

CMTimeConvertScale = c.CMTimeConvertScale
CMTimeConvertScale.argtypes = [CMTime, c_int32]
CMTimeConvertScale.restype = CMTime

CMTimeMultiplyByRatio = c.CMTimeMultiplyByRatio
CMTimeMultiplyByRatio.argtypes = [CMTime, c_int32, c_int32]
CMTimeMultiplyByRatio.restype = CMTime

CMTimeCompare = c.CMTimeCompare
CMTimeCompare.argtypes = [CMTime, CMTime]
CMTimeCompare.restype = c_int32

def objc_CMTime(struct):
    '''Converts the AnonymousStructure fromn the returns of some objc functions'''
    return CMTime(struct.a, struct.b, struct.c, struct.d)
