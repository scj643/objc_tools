from objc_tools.displays import getScreens
from objc_util import ObjCInstance, ObjCClass
import ui

UIWindow = ObjCClass("UIWindow")


class ExternalView (ui.View):
    def __init__(self, external):
        self.external = external
    
    def will_close(self):
        self.external.close()
    
    
class External (object):
    '''A class that presents a view on an external display'''
    def __init__(self, screen):
        self.screen = screen
        self.window = UIWindow.alloc().initWithFrame_(screen.objc.bounds())
        self.view = ExternalView(self)
        
        
    def close(self):
        pass
