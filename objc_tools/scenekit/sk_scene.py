from objc_util import ObjCClass, load_framework, nsurl, ObjCInstance
from objc_tools.scenekit.util import SUPPORTED_FORMATS, LightType, ShadowMode, DebugOptions
from objc_tools.scenekit.structures import Vector3, Vector4, Matrix4
import ui


load_framework('SceneKit')
load_framework('SpriteKit')


SCNScene = ObjCClass('SCNScene')
SCNNode = ObjCClass('SCNNode')
SCNLight = ObjCClass('SCNLight')
SCNView = ObjCClass('SCNView')


class SceneView (ui.View):
    def __init__(self):
        self._scene_objc = SCNView.alloc().initWithFrame_options_(((0, 0),(100, 100)), None).autorelease()
        self._scene_objc.setAutoresizingMask_(18) # Fill superview
        ObjCInstance(self).addSubview_(self._scene_objc)
        self._scene_objc.setNeedsDisplayOnBoundsChange_(True) # fill on change
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
        
    @property
    def debugOptions(self):
        return DebugOptions(self._scene_objc.debugOptions())
        
    @debugOptions.setter
    def debugOptions(self, value):
        if isinstance(value, (DebugOptions)):
            self._scene_objc.setDebugOptions_(value.value)
        else:
            self._scene_objc.setDebugOptions_(int(value))
            
    def stop(self):
        self._scene_objc.stop_(None)

    def pause(self):
        self._scene_objc.pause_(None)

    def play(self):
        self._scene_objc.play_(None)
        

class Scene (object):
    def __init__(self, scene = SCNScene.scene()):
        self._objc = scene
        self._node_ref = Node(self._objc.root())
        
    @property
    def playbackSpeed(self):
        return self._objc.playbackSpeed()
    
    @playbackSpeed.setter
    def playbackSpeed(self, value):
        self._objc.setPlaybackSpeed_(value)
    
    @property
    def framerate(self):
        return self._objc.frameRate()
        
    @framerate.setter
    def framerate(self, value):
        self._objc.setFrameRate_(value)
        
    @property
    def fogDensityExponent(self):
        '''
        Controls the attenuation between the start and end fog distances.
        0 means a constant fog, 1 a linear fog and 2 a quadratic fog,
        but any positive value will work.
        '''
        return self._objc.fogDensityExponent()
        
    @fogDensityExponent.setter
    def fogDensityExponent(self, value):
        self._objc.setFogDensityExponent_(value)
    
    @property
    def fogStartDistance(self):
        return self._objc.fogStartDistance()
        
    @fogStartDistance.setter
    def fogStartDistance(self, value):
        self._objc.setFogStartDistance_(value)
        
    @property
    def fogEndDistance(self):
        return self._objc.fogEndDistance()
        
    @fogEndDistance.setter
    def fogEndDistance(self, value):
        self._objc.setFogEndDistance_(value)
        
    @property
    def paused(self):
        return self._objc.isPaused()
        
    @paused.setter
    def paused(self, value):
        self._objc.setPaused_(value)
        
    @property
    def node(self):
        if self._node_ref._objc.ptr == self._objc.root().ptr: # checks so we domt use more memory
            return self._node_ref
        else:
            self._node_ref = Node(self._objc.root())
            return self._node_ref
        
    def removeAllParticleSystems(self):
        self._objc.removeAllParticleSystems()
        
    def save_to_file(self, path):
        if SUPPORTED_FORMATS.match(path.rsplit('.', 1)[-1]):
            options = ns({'SCNSceneExportDestinationURL': nsurl(path)})
            url = nsurl(path)
            self._objc.writeToURL_options_(url, options)
        else:
            raise TypeError('Not a supported export type')
            
    def __repr__(self):
        return '<Scene <Framerate: {}, node: {}>>'.format(self.framerate, self.node)
        

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



