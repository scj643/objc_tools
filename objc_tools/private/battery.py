from objc_util import ObjCInstance, c
from ctypes import c_char_p, c_long, c_int, c_void_p, c_int32, c_int64, byref, c_uint
from datetime import datetime
from objc_tools.objc_json import objc_to_py
from objc_tools.c.objc_handler import chandle
__all__ = ['Battery']

IOServiceMatching = c.IOServiceMatching
IOServiceMatching.argtypes=[c_char_p]
IOServiceMatching.restype = c_long
IOServiceMatching.errcheck = chandle

IORegistryGetRootEntry = c.IORegistryGetRootEntry
IORegistryGetRootEntry.argtypes = [c_int]
IORegistryGetRootEntry.restype = c_void_p

kIOMasterPortDefault=c_int.in_dll(c,'kIOMasterPortDefault')

# srv=ObjCInstance(IOServiceMatching(b"IOPMPowerSource"))
srv=IOServiceMatching(b"IOPMPowerSource")

IOServiceGetMatchingService = c.IOServiceGetMatchingService
IOServiceGetMatchingService.argtypes=[c_int, c_void_p]
IOServiceGetMatchingService.restype = c_uint

powerSource = IOServiceGetMatchingService(kIOMasterPortDefault, srv);
#c.IOServiceGetMatchingService
IORegistryEntryCreateCFProperties = c.IORegistryEntryCreateCFProperties
IORegistryEntryCreateCFProperties.argtypes=[c_int64 ,c_void_p, c_void_p, c_int32 ]

IORegistryEntryCreateCFProperty = c.IORegistryEntryCreateCFProperty
IORegistryEntryCreateCFProperty.argtypes = [c_void_p, c_void_p, c_void_p, c_int32]
IORegistryEntryCreateCFProperty.restype = c_void_p

#c.IORegistryEntryCreateCFProperty(service, ns('IOPlatformSerialNumber'), 0, 0)

class Battery (object):
    '''A Battery Object:
       The reason for this is to make releasing said object a lot easier'''
       
    def __init__(self):
        self.update()
    
    def update(self):
        '''Update the information in the object'''
        self._objc_ptr=c_void_p(0)
        IORegistryEntryCreateCFProperties(powerSource, byref(self._objc_ptr), None, 0)
        self.timestamp = datetime.now()
        self.valid = True
        
    def objc(self):
        if self._objc_ptr:
            return ObjCInstance(self)
        else:
            raise ValueError('Operation on released object')
    
    def release(self):
        ObjCInstance(self).release()
        self.valid = False
        self._objc_ptr = None
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
        
    def __enter__(self):
        self.__init__()
        return self
        
    def get_dict(self):
        i = objc_to_py(self.objc())
        i['timestamp'] = self.timestamp
        return i
        
    def __repr__(self):
        return '<Battery info at time {}, Valid: {}>'.format(self.timestamp.__str__(), self.valid)
        
    def update_and_return(self):
        '''Updates the object and returns a dict
           Useful for live monitoring'''

        self.update()
        return self.get_dict()
