from objc_tools.ui.displays import getScreens
from objc_util import ObjCInstance, ObjCClass
import ui

UIWindow = ObjCClass("UIWindow")


class ExternalView (ui.View):
    '''An ExternalView View
    external: A External Object
    '''
    def __init__(self, external):
        self.external = external
        self.width = external.screen.currentMode.size[0]
        self.height = external.screen.currentMode.size[1]
    def will_close(self):
        self.external.close()
    
    
class External (object):
    '''A class that presents a view on an external display
    screen: The screen to display on
    '''
    def __init__(self, screen):
        self.screen = screen
        '''This contains all the subviews'''
        self.window = UIWindow.alloc().initWithFrame_(screen.objc.bounds())
        self.view = ExternalView(self)
        self.window.addSubview_(ObjCInstance(self.view))
        
        
    def close(self):
        pass
