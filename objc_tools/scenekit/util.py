import re
from objc_tools.backports.enum_backport import Flag, IntEnum
from objc_util import Structure, c_float
from pprint import pformat

SUPPORTED_FORMATS = re.compile('dae|scn', re.I)

class LightType (object):
    Ambient = 'ambient'
    Omni = 'omni'
    Directonal = 'directional'
    Spot = 'spot'
    IES = 'IES'
    Probe = 'probe'


class LightingModel (object):
    Phong = 'SCNLightingModelPhong'
    Lambert = 'SCNLightingModelLambert'
    Constant = 'SCNLightingModelConstant'
    PhysicallyBased = 'SCNLightingModelPhysicallyBased'
    Blinn = 'SCNLightingModelBlinn'
    

class ShadowMode (IntEnum):
    '''See apple documentation'''
    forward = 0
    deferred = 1
    modulated = 2


class GeometryPrimitiveType (IntEnum):
    triangles = 0
    triangleStrip = 1
    line = 2
    point = 3


class CullMode (IntEnum):
    back = 0
    front = 1
    

class TransparencyMode (IntEnum):
    AOne = 0
    RGBZero = 1


class BlendMode (IntEnum):
    alpha = 0 # Blends the source and destination colors by adding the source multiplied by source alpha and the destination multiplied by one minus source alpha.
    add = 1 # Blends the source and destination colors by adding them up.
    subtract = 2 # Blends the source and destination colors by subtracting the source from the destination.
    multiply = 3 # Blends the source and destination colors by multiplying them.
    screen = 4 # Blends the source and destination colors by multiplying one minus the source with the destination and adding the source.
    replace = 5 #Replaces the destination with the source (ignores alpha).


class FilterMode (IntEnum):
    none = 0
    nearest = 1
    linear = 2

class WrapMode (IntEnum):
    clamp = 1
    repeat = 2
    clampToBorder = 3
    mirror = 4


class SCNMovabilityHint (IntEnum):
    fixed = 0
    movable = 1
    

class SCNPhysicsBodyType (IntEnum):
    static = 0
    dynamic = 1
    kinematic = 2

    
class SCNPhysicsCollisionCategory (Flag):
    default = 1 << 0 # default collision group for dynamic and kinematic objects
    static = 1 << 1 # default collision group for static objects
    all = 0 # default for collision mask


class PhysicsFieldScope (IntEnum):
    '''
    Specifies the domain of influence of a physics field.
    '''
    insideExtent = 0
    outsideExtent = 1


class ReferenceLoadingPolicy (IntEnum):
    '''
    Controls whenever to load the reference node
    '''
    immediate = 0
    onDemand = 1


class AntialiasingMode (IntEnum):
    none = 0
    multisampling2X = 1
    multisampling4X = 2


class DebugOptions (Flag):
    none = 0
    showPhysicsShapes = 1 << 0
    showBoundingBoxes = 1 << 1
    showLightInfluences = 1 << 2
    showLightExtents = 1 << 3
    showPhysicsFields = 1 << 4
    showWireframe = 1 << 5


class RenderingAPI (IntEnum):
    metal = 0
    openGLES2 = 1


