from objc_util import ObjCClass
UIDevice = ObjCClass('UIDevice')
NSProcessInfo = ObjCClass('NSProcessInfo')
device = UIDevice.currentDevice()
process = NSProcessInfo.processInfo()
_fsizes = {'B': 1.0, 'KB': 1024.0, 'MB':  float(pow(1024,2)), 'GB': float(pow(1024,3))}


class Process (object):
    def __init__(self):
        self._objc = NSProcessInfo.processInfo()
        self._fsizes = {'B': 1.0, 'KB': 1024.0, 'MB':  float(pow(1024,2)), 'GB': float(pow(1024,3))}
    @property
    def lowPowerModeStatus(self):
        return self._objc.isLowPowerModeEnabled()
        
    @property
    def hostName(self):
        return str(self._objc.hostName())
        
    @property
    def osVersion(self):
        major = self._objc.operatingSystemVersion().a
        minor = self._objc.operatingSystemVersion().b
        patch = self._objc.operatingSystemVersion().c
        return (major, minor, patch)
    
    @property
    def osVersionString(self):
        return str(self._objc.operatingSystemVersionString())
    
    @property
    def physicalMemory(self, unit='MB'):
        if unit in self._fsizes:
            divider = self._fsizes[unit]
        else:
            divider = self._fsizes['MB']
        mem = int(self._objc.physicalMemory())
        return mem/float(divider)
        
    @property
    def processName(self):
        return str(self._objc.processName())
        
    @processName.setter
    def processName(self, value):
        if type(value) == str:
            self._objc.setProcessName_(value)
    
    @property
    def activeProcessors(self):
        return self._objc.activeProcessorCount()
        
    @property
    def pid(self):
        return self._objc.processIdentifier()
        
    @property
    def enviornment(self):
        p = self._objc.environment()
        keys = []
        values = []
        returns = {}
        for i in p.allKeys():
            keys += [str(i)]
        for i in p.allValues():
            values += [str(i)]
        for i in zip(keys, values):
            returns[i[0]] = i[1]
        return returns
    
    @property
    def systemUptime(self):
        '''
        Returns system uptime in seconds
        '''
        return self._objc.systemUptime()


class Device (object):
    def __init__(self):
        self._objc = UIDevice.currentDevice()
        
    @property
    def deviceName(self):
        return str(device.name())
        
    @property
    def deviceType(self):
        return str(self._objc.model())
        
    @property
    def supportsForceTouch(self):
        '''Checks if force touch is supported
        Private API may break
        '''
        return self._objc._supportsForceTouch()
        
    @property
    def supportsDeepColor(self):
        '''Checks if deep color is supported
        This is currently only on the iPad Pro 9.7 inch
        Private API may break
        '''
        return self._objc._supportsDeepColor()

