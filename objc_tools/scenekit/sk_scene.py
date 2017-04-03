from objc_util import ObjCClass, load_framework, nsurl
from objc_tools.scenekit.util import SUPPORTED_FORMATS
from objc_tools.scenekit.structures import Vector3, Vector4, Matrix4
from objc_tools.scenekit.node import Node
load_framework('SceneKit')
load_framework('SpriteKit')

SCNScene = ObjCClass('SCNScene')
SCNNode = ObjCClass('SCNNode')


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



