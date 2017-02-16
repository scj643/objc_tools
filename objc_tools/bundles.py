from objc_util import NSBundle, ObjCInstance, ObjCClass
from os import listdir
from glob import glob
__doc__ = '''A tool for working with NSBundle'''
FRAMEWORK_PATH = '/System/Library/Frameworks/'
PRIVATE_FRAMEWORK_PATH = '/System/Library/PrivateFrameworks/'


class Bundle (object):
    def __init__(self, bundle):
        self.objc = bundle
        
    @property
    def isLoaded(self):
        return self.objc.isLoaded()
    
    @property
    def versionNumber(self):
        return self.objc.versionNumber()
        
    @property
    def infoDictionary(self):
        return self.objc.infoDictionary()
        
    @property
    def bundleID(self):
        try:
            returns = str(self.objc.bundleIdentifier())
        except:
            returns = 'Unknown'
        return returns
        
    @property
    def path(self):
        return str(self.objc.bundlePath())
        
    @property
    def isLoaded(self):
        return self.objc.isLoaded()
        
    @property
    def extensionType(self):
        return self.path.rsplit('.',1)[-1]
        
    def load(self):
        return self.objc.load()
        
    def unload(self):
        return self.objc.unload()
    
    @property
    def primcipleClass(self):
        if self.objc.principalClass():
            return ObjCInstance(self.objc.principalClass())
        else:
            return None
        
    def __repr__(self):
        return '<Framework <{}> (Path {}) Loaded: {}>'.format(self.bundleID, self.path, self.isLoaded)
        
        
def getLoadedFrameworks():
    blist = []
    for i in NSBundle.allFrameworks():
        if i.isLoaded():
            blist += [Bundle(i)]
    return blist
    
    
def getBundleWithID(bid):
    return Bundle(NSBundle.bundleWithIdentifier_(bid))
    
    
def bundleForObjcClass(objc):
    return Bundle(NSBundle.bundleForClass_(objc))
    

def unloadedFrameworks():
    pass
    

def listPublicFrameworks():
    returns = []
    for i in listdir(FRAMEWORK_PATH):
        returns += [getBundleWithPath(FRAMEWORK_PATH+i)]
    return returns
    

def listPrivateFrameworks():
    returns = []
    for i in listdir(PRIVATE_FRAMEWORK_PATH):
        returns += [getBundleWithPath(PRIVATE_FRAMEWORK_PATH+i)]
    return returns    
    

def getBundleWithPath(path):
    return Bundle(NSBundle.bundleWithPath_(path))
    
    
def getBundlesAtPath(path, recursive = True, kind = 'framework'):
    '''Get all bundles at a path
    path: the path you want to search
    recursive: go into subdirectories
    kind: used to determine what the extension to search for is.
    '''
    returns = []
    for i in glob('{}/**/*.{}/'.format(path, kind), recursive = True):
        returns += [getFrameworkWithPath(i)]
    return returns
    

def bundleForClass(cls):
    if type(cls) == str:
        try:
            cls = ObjCClass(cls)
        except:
            return None
        
    try:
        b=NSBundle.bundleForClass_(cls)
        return Bundle(b)
    except ValueError:
        return None
