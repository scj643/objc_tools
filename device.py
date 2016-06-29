from objc_util import ObjCClass
UIDevice = ObjCClass('UIDevice')
NSProcessInfo = ObjCClass('NSProcessInfo')
device = UIDevice.currentDevice()
process = NSProcessInfo.processInfo()
_fsizes = {'B': 1.0, 'KB': 1024.0, 'MB':  float(pow(1024,2)), 'GB': float(pow(1024,3))}

def lowPowerModeStatus():
    return process.isLowPowerModeEnabled()
    

def hostName():
    return str(process.hostName())
    

def osVersion():
    major = process.operatingSystemVersion().a
    minor = process.operatingSystemVersion().b
    patch = process.operatingSystemVersion().c
    return (major, minor, patch)


def osVersionString():
    return str(process.activeProcessorCount())


def deviceName():
    return str(device.name())


def deviceType():
    return str(device.model())


def deviceGeneration():
    return str(device._currentProduct())

    
def activeProcessors():
    return process.activeProcessorCount()


def physicalMemory(unit='MB'):
    if unit in _fsizes:
        divider = _fsizes[unit]
    else:
        divider = _fsizes['MB']
    mem = int(process.physicalMemory())
    return mem/float(divider)


def processorCount():
    return process.processorCount()


def setProcessName(name):
    if type(name) == str:
        process.setProcessName_(name)
        return True
    else:
        return False


def processName():
    return str(process.processName())
    

def systemUptime():
    '''
    Returns system uptime in seconds
    '''
    return process.systemUptime()



