from objc_util import ObjCClass
UIDevice = ObjCClass('UIDevice')
NSProcessInfo = ObjCClass('NSProcessInfo')
device = UIDevice.currentDevice()
process = NSProcessInfo.processInfo()

def lowPowerModeStatus():
    return process.isLowPowerModeEnabled()
    

def hostName():
    return str(process.hostName())
    

def osVersion():
    major = process.operatingSystemVersion().a
    minor = process.operatingSystemVersion().b
    patch = process.operatingSystemVersion().c
    return (major, minor, patch)
    

def deviceName():
    return str(device.name())
    

def deviceType():
    return str(device.model())
