from objc_util import ObjCClass, load_framework, nsurl, ObjCInstance
from objc_tools.scenekit.structures import *
from objc_tools.scenekit.util import LightType, ShadowMode
from objc_tools.scenekit.physics import *
load_framework('SceneKit')
load_framework('SpriteKit')

SCNNode = ObjCClass('SCNNode')
SCNLight = ObjCClass('SCNLight')


class Node (object):
    def __init__(self, node = SCNNode.node()):
        self._objc = node
        self._light = None

    @property
    def name(self):
        return str(self._objc.name())

    @name.setter
    def name(self, value):
        self._objc.setName_(value)
        
    @property
    def transform(self):
        '''transfrom
        Note: with this you can not set properties directly
        '''
        return self._objc.transform(argtypes = [], restype = Matrix4)
        
    @transform.setter
    def transform(self, value):
        self._objc.setTransform_(value, argtypes = [Matrix4], restype = None)
        
    @property
    def position(self):
        return self._objc.position(argtypes = [], restype = Vector3)
    
    @position.setter
    def position(self, value):
        self._objc.setPosition_(value, argtypes = [Vector3], restype = None)
        
    @property
    def rotation(self):
        return self._objc.rotation()
        
    @rotation.setter
    def rotation(self, value):
        self._objc.setRotation_(value)
        
    @property
    def light(self):
        return self._light
            
    @light.setter
    def light(self, value):
        if isinstance(value, (ObjCInstance)):
            self._objc.setLight_(value)
            self._light = Light(value)
        if isinstance(value, (Light)):
            self._objc.setLight_(value._objc)
            self._light = value
        if value == None:
            self._objc.setLight_(value)
            self._light = value
    
    
    def clone(self):
        '''clone
        The copy is recursive: every child node will be cloned, too.
        The copied nodes will share their attached objects (light, geometry, camera, ...) with the original instances
        '''
        return Node(self._objc.clone())
    
    def flattenedClone(self):
        '''flattenedCLone
        A copy of the node with all geometry combined
        '''
        return Node(self._objc.flattenedClone())


class Light (object):
    def __init__(self, kind = LightType.Omni, objc = SCNLight.light()):
        self._objc = objc
        self.type = kind
        
    @property
    def type(self):
        return self._objc.type()
    
    @type.setter
    def type(self, kind):
        self._objc.setType_(kind)
        
    @property
    def castsShadow(self):
        return self._objc.castsShadow()
    
    @castsShadow.setter
    def castsShadow(self, value):
        self._objc.setCastsShadow_(value)
        
    @property
    def intensity(self):
        return self._objc.intensity()
        
    @intensity.setter
    def intensity(self, value):
        self._objc.setIntensity_(value)
