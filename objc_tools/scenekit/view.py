from objc_util import load_framework, ObjCClass, ObjCInstance
from objc_tools.scenekit.sk_scene import Scene
from objc_tools.scenekit.node import *
import ui

load_framework('SceneKit')
load_framework('SpriteKit')

SCNView = ObjCClass('SCNView')


class SceneView (ui.View):
    def __init__(self):
        self._scene_objc = SCNView.alloc().initWithFrame_options_(((0, 0),(100, 100)), None).autorelease()
        self._scene_objc.setAutoresizingMask_(18) # Fill superview
        ObjCInstance(self).addSubview_(self._scene_objc)
        self._scene_ref = None
    
    @property
    def showsStatistics(self):
        return self._scene_objc.showsStatistics()

    @showsStatistics.setter
    def showsStatistics(self, state):
        if type(state) == bool:
            self._scene_objc.setShowsStatistics_(state)
        else:
            raise TypeError('Must be a bool')

    @property
    def preferredFramesPerSecond(self):
        return self._scene_objc.preferredFramesPerSecond()

    @preferredFramesPerSecond.setter
    def preferredFramesPerSecond(self, value):
        self._scene_objc.setPreferredFramesPerSecond_(value)

    @property
    def allowsCameraControl(self):
        return self._scene_objc.allowsCameraControl()
        
    @allowsCameraControl.setter
    def allowsCameraControl(self, state):
        if type(state) == bool:
            self._scene_objc.setAllowsCameraControl_(state)
        else:
            raise TypeError('Must be a bool')
            
    @property
    def scene(self):
        if self._scene_ref:
            return self._scene_ref
        elif self._scene_objc.scene():
            raise Warning('The scene does not have a reference')
            return Scene(self._scene_objc.scene())
        else:
            return None
    
    @scene.setter
    def scene(self, value):
        if isinstance(value, (Scene)):
            self._scene_ref = value
            self._scene_objc.setScene_(value._objc)
        elif isinstance(value, (ObjCInstance)):
            self._scene_ref = Scene(value)
            self._scene_objc.setScene_(value)
        else:
            raise TypeError("Not able to set scene")
            
    def stop(self):
        self._scene_objc.stop_(None)

    def pause(self):
        self._scene_objc.pause_(None)

    def play(self):
        self._scene_objc.play_(None)

