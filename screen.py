from objc_util import *
from objc_tools.pythonista_tool import backgroundTimeRemaining
UIScreen = ObjCClass('UIScreen')
UIWindow = ObjCClass('UIWindow')
UIView = ObjCClass('UIView')

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
        
        
class UIScreenMode (object):
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
        self.objc = screen
        self.bitDepth = screen.bitsPerComponent()
        self.modes = []
        for i in screen.availableModes():
            self.modes += [UIScreenMode(i)]
        self.currentMode = UIScreenMode(screen.currentMode())
        self.nativeScale = screen.nativeScale()
        try:
            self.ScreenName = str(screen._name())
        except:
            self.ScreenName = None
            raise NotImplementedError('Private api _name not avalible')
        try:
            self.orientation = screen._interfaceOrientation()
        except:
            self.orientation = None
            raise NotImplementedError('Private api _interfaceOrientation not avalible')
    
    
    def getBrightness(self):
       return self.objc.brightness()
       
       
    def setBrightness(self, level):
        '''Set the display's brightness
        Is a number between 0 and 1 any higher ends up maxing and any lower casues it to min
        Ex. -1 will really be equal to 0
        Ex. 2 will really be equal to 1
        '''
        self.objc.setBrightness_(level)


    def getSnapshot(self):
        '''Get a snapshot of the screen
        Returns a UIView compatable view
        Can be added as a subview
        '''
        return self.objc.snapshot()

    def __repr__(self):
        return str(self.objc.description()).replace('UIScreen', 'Screen')
       
def getScreens():
    returns = []
    for i in list(UIScreen.screens()):
        returns += [Screen(i)]
    return returns
    

if __name__ == '__main__':
    s = getScreens()[1]
