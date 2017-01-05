from objc_util import *
UIScreen = ObjCClass('UIScreen')


def processCGSize(size):
    return (size.width, size.height)
    

class Display (object):
    def __init__(self, display):
        self.objc = display
        self.allowsVirtualModes = display.allowsVirtualModes()
        self.name = display.name()
        self.deviceName = display.deviceName()
        self.supportsExtendedColors = display.supportsExtendedColors()
        self.isCloned = display.isCloned()
        self.isCloningSupported = display.isCloningSupported()
        self.isExternal = display.isExternal()
        self.isOverscanned = display.isOverscanned()
        
class DisplayMode (object):
    def __init__(self, displayMode):
        self.colorMode = str(displayMode.colorMode())
        self.isVirtual = displayMode.isVirtual()
        self.refreshRate = displayMode.refreshRate()
        self.objc = displayMode
        
        
class UIMode (object):
    def __init__(self, mode, initDisplayInfo=True):
        self.objc = mode
        self.pixelAspectRatio = mode.pixelAspectRatio()
        self.size = processCGSize(mode.size())
        if initDisplayInfo:
            self.initDisplayMode()
        else:
            self.displayMode = None
        
    def initDisplayMode(self):
        try:
            self.displayMode = DisplayMode(self.objc._displayMode())
        except:
            self.displayMode = None
            raise NotImplementedError('Private api _diplayMode not avalible')
        

class Screen (object):
    def __init__(self, screen):
        self.bitDepth = screen.bitsPerComponent()
        self.modes = list(screen.availableModes())
