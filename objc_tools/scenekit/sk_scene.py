from objc_util import ObjCClass, load_framework, nsurl, ObjCInstance, on_main_thread, ns, create_objc_class, UIApplication, UIColor, CGSize
from objc_tools.scenekit.util import SUPPORTED_FORMATS, LightType, ShadowMode, DebugOptions, RenderingAPI, LightingModel
from objc_tools.scenekit.structures import Vector3, Vector4, Matrix4
from objc_tools.ui.editorview import TabView, tabVC
import ui
from math import pi


load_framework('SceneKit')
load_framework('SpriteKit')


SCNScene = ObjCClass('SCNScene')
SCNNode = ObjCClass('SCNNode')
SCNLight = ObjCClass('SCNLight')
SCNView = ObjCClass('SCNView')
SCNCamera = ObjCClass('SCNCamera')
UIViewController = ObjCClass('UIViewController')
SCNMaterial = ObjCClass('SCNMaterial')

        
class SKView (object):
    '''SKView
    This object is used for subclassing
    '''
    def __init__(self):
        self._create_objc()
        self.attach()
    
    def _create_objc(self):
        self._scene_objc = SCNView.alloc().initWithFrame_options_(((0, 0),(100, 100)), ns({'SCNViewOptionPreferredRenderingAPI': 1})).autorelease()
        self._scene_objc.setAutoresizingMask_(18) # Fill superview
        self._scene_objc.setNeedsDisplayOnBoundsChange_(True) # fill on change
        self._scene_ref = None
        self._pointOfView_ref = Node(self._scene_objc.pointOfView())
        
    def attach(self):
        '''attach
        This function is called after __init__
        '''
        pass
    
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
            
    @property
    def pointOfView(self):
        if self._scene_objc.pointOfView().ptr != self._pointOfView_ref._objc.ptr:
            self._pointOfView_ref = Node(self._scene_objc.pointOfView())
        return self._pointOfView_ref
    
    def setPointOfView(self, value, animate = True):
        if isinstance(value, (ObjCInstance)):
            self._pointOfView_ref = Node(value)
            self._scene_objc.setPointOfView_animate_(value, animate)
        if isinstance(value, (Node)):
            self._pointOfView_ref = value
            self._scene_objc.setPointOfView_animate_(value._objc, animate)
        
    def stop(self):
        self._scene_objc.stop_(None)

    def pause(self):
        self._scene_objc.pause_(None)

    def play(self):
        self._scene_objc.play_(None)


class SceneView (SKView):
    def attach(self):
        self.uiView = ui.View()
        self.present = self.uiView.present
        ObjCInstance(self.uiView).addSubview_(self._scene_objc)

class SceneTab (SceneView, TabView):
    def __init__(self):
        SceneView.__init__(self)
        TabView.__init__(self)
        
    @on_main_thread
    def makeSelf(self):
        self.name = "SceneKit"
        
    @on_main_thread
    def customVC(self):
        return create_objc_class(
                "CustomViewController",
                UIViewController,
                methods=[],
                protocols=["OMTabContent"],
        ).new()
        
    @on_main_thread
    def show(self):
        self.newVC.View = ObjCInstance(self.uiView)
        self.newVC.title = self.name
        self.newVC.navigationItem().rightBarButtonItems = self.right_button_items
        tabVC.addTabWithViewController_(self.newVC)
        


class Scene (object):
    def __init__(self, scene = None):
        if scene:
            self._objc = objc
        else:
            self._objc = SCNScene.scene()
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
        
    def save_to_file(self, file_name):
        if SUPPORTED_FORMATS.match(path.rsplit('.', 1)[-1]):
            options = ns({'SCNSceneExportDestinationURL': nsurl(path)})
            file = nsurl(file_name)
            
            return self._objc.writeToURL_options_(url, options)
        else:
            raise TypeError('Not a supported export type')
            
    def __repr__(self):
        return '<Scene <Framerate: {}, node: {}>>'.format(self.framerate, self.node)
        

class Node (object):
    def __init__(self, objc = None):
        self._light = None
        self._geometry = None
        self._camera = None
        self._child_ref = []
        if objc:
            self._objc = objc
            if self._objc.light():
                self._light = Light(objc=self._objc.light())
            if self._objc.geometry():
                self._geometry = Geometry(self._objc.geometry())
            if self._objc.camera():
                self._camera = Camera(self._objc.camera())
        else:
            self._objc = SCNNode.node()
        
    @property
    def childNodes(self):
        return self._child_ref

    @property
    def name(self):
        if self._objc.name():
            return str(self._objc.name())
        else:
            return None
    
    @name.setter
    def name(self, value):
        self._objc.setName_(value)
        
    @property
    def scale(self):
        return self._objc.scale()
    
    @scale.setter
    def scale(self, value):
        self._objc.setScale_(value)
        
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
    
    @property
    def geometry(self):
        return self._geometry
        
    @geometry.setter
    def geometry(self, value):
        if isinstance(value, (ObjCInstance)):
            self._objc.setGeometry_(value)
            self._geometry = Geometry(value)
        if isinstance(value, (Geometry)):
            self._objc.setGeometry_(value._objc)
            self._light = value
        if value == None:
            self._objc.setGeometry_(value)
            self._light = value
    
    @property
    def camera(self):
        return self._camera
        
    @camera.setter
    def camera(self, value):
        if isinstance(value, (ObjCInstance)):
            self._objc.setCamera_(value)
            self._camera = Camera(value)
        if isinstance(value, (Camera)):
            self._objc.setCamera_(value._objc)
            self._camera = value
        if value == None:
            self._objc.setCamera_(value)
            self._camera = value
    
    def clone(self):
        '''clone
        The copy is recursive: every child node will be cloned, too.
        The copied nodes will share their attached objects (light, geometry, camera, ...) with the original instances
        '''
        clone = self._objc.clone()
        return Node(clone)
    
    def flattenedClone(self):
        '''flattenedCLone
        A copy of the node with all geometry combined
        '''
        clone = self._objc.flattenedClone()
        return Node(clone)
        
    def addChild(self, value):
        if isinstance(value, (ObjCInstance)):
            if self._objc.canAddChildNode_(value):
                self._objc.addChildNode_(value)
                self._child_ref += [Node(value)]
        if isinstance(value, (Node)):
            if self._objc.canAddChildNode_(value._objc) and value not in self._child_ref:
                self._objc.addChildNode_(value._objc)
                self._child_ref += [value]


class Light (object):
    def __init__(self, kind = LightType.Omni, casts_shadow = True, shadow_sample_count = 1000, objc = None):
        if objc:
            self._objc = objc
        else:
            self._objc = SCNLight.light()
            self.type = kind
            self.castsShadow = casts_shadow
            self.shadowSampleCount = shadow_sample_count
        
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
        
    @property
    def shadowSampleCount(self):
        return self._objc.shadowSampleCount()
        
    @shadowSampleCount.setter
    def shadowSampleCount(self, value):
        self._objc.setShadowSampleCount_(value)
    
    @property
    def name(self):
        if self._objc.name():
            return str(self._objc.name())
        else:
            return None
    
    @name.setter
    def name(self, value):
        self._objc.setName_(value)
        
    @property
    def color(self):
        return self._objc.color()
        
    @color.setter
    def color(self, value):
        self._objc.setColor_(value)

    @property
    def shadowColor(self):
        return self._objc.color()
        
    @shadowColor.setter
    def shadowColor(self, value):
        self._objc.setShadowColor_(value)
        
    @property
    def shadowRadius(self):
        return self._objc.shadowRadius()
    
    @shadowRadius.setter
    def shadowRadius(self, value):
        self._objc.setShadowRadius(value)
        
    @property
    def shadowMapSize(self):
        return self._objc.shadowMapSize()
    
    @shadowMapSize.setter
    def shadowMapSize(self, value):
        self._objc.setShadowMapSize(value)
    
class Camera (object):
    def __init__(self, objc = None):
        if objc:
            self._objc = objc
        else:
            self._objc = SCNCamera.camera()
            
    @property
    def name(self):
        if self._objc.name():
            return str(self._objc.name())
        else:
            return None
    
    @name.setter
    def name(self, value):
        self._objc.setName_(value)
        
    @property
    def xFov(self):
        '''Setting to 0 resets it to normal'''
        return self._objc.xFov()
    
    @xFov.setter
    def xFov(self, value):
        self._objc.setXFov_(value)
        
    @property
    def yFov(self):
        '''Setting to 0 resets it to normal'''
        return self._objc.yFov()
    
    @yFov.setter
    def yFov(self, value):
        self._objc.setYFov_(value)
        
class Geometry (object):
    def __init__(self, objc = None):
        self._objc = objc
    
    @property
    def name(self):
        if self._objc.name():
            return str(self._objc.name())
        else:
            return None
    
    @name.setter
    def name(self, value):
        self._objc.setName_(value)
    
    @property
    def material(self):
        return Material(self._objc.material())


class Material (object):
    def __init__(self, objc = None):
        self._objc = objc
        
    @property
    def lightingModel(self):
        return str(self._objc.lightingModelName())

    @lightingModel.setter
    def lightingModel(self, value):
        if type(value) == str:
            self._objc.setLightingModelName_(value)
        else:
            print('not a valid type')
        
def load_scene(file):
    url = ns(file)
    s = SCNScene.sceneWithURL_options_(url, ns({}))
    return Scene(s)
                
if __name__ == '__main__':
    for i in UIApplication.sharedApplication().keyWindow().rootViewController().view().gestureRecognizers():
            if b'UIPanGestureRecognizer' == i._get_objc_classname():
                slide = i
    slide.setEnabled_(False)
    SCNLookAtConstraint = ObjCClass('SCNLookAtConstraint')
    
    v = SceneTab()
    v.allowsCameraControl=True
    SCNBox = ObjCClass('SCNBox')
    SCNFloor = ObjCClass('SCNFloor')
    SCNSphere = ObjCClass('SCNSphere')
    v.debugOptions = DebugOptions.showLightInfluences| DebugOptions.showLightExtents
    v.showsStatistics=True
    v.scene = Scene()
    floor = SCNFloor.floor()
    cnode = Node()
    c = Camera()
    cnode.camera = c
    v.scene.node.addChild(cnode)
    n=Node()
    pnode = Node()
    sphere = Node()
    pnode.geometry = floor
    pnode.geometry.material.lightingModel = LightingModel.PhysicallyBased
    v.scene.node.addChild(pnode)
    n.geometry = SCNBox.boxWithWidth_height_length_chamferRadius_(5,5,5,0)
    n.position = Vector3(0,2.511,0)
    sphere.geometry = SCNSphere.sphereWithRadius_(2)
    sphere.geometry.material.lightingModel = LightingModel.PhysicallyBased
    n.geometry.material.lightingModel = LightingModel.PhysicallyBased
    v.scene.node.addChild(n)
    l = Node()
    l.position = Vector3(25,25,20)
    l.rotation = Vector4(1,0,0,-pi/2)
    l.light = Light('spot')
    con=SCNLookAtConstraint.lookAtConstraintWithTarget_(n._objc)
    l._objc.setConstraints_([con])
    #cnode._objc.setConstraints_([con])
    v.scene.node.addChild(n)
    v.scene.node.addChild(l)
    v.scene._objc.background().setColor_(UIColor.colorWithName_('black'))
    v.show()
    cl = l.clone()
