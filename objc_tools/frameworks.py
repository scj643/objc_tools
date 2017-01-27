from objc_util import *
from os import listdir
FRAMEWORK_PATH = '/System/Library/Frameworks/'
PRIVATE_FRAMEWORK_PATH = '/System/Library/PrivateFrameworks/'


class Framework (object):
    def __init__(self, bundle):
        self.objc = bundle
        
    @property
    def isLoaded(self):
        return self.objc.isLoaded()
    
    @property
    def versionNumber(self):
        return self.objc.versionNumber()
        
    @property
    def infoDictionary():
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
        
    def getExtensionType(self):
        return self.path.rsplit('.',1)[-1]
        
    def load(self):
        return self.objc.load()
        
    def unload(self):
        return self.objc.unload()
        
    def __repr__(self):
        return '<Framework <{}> (Path {}) Loaded: {}>'.format(self.bundleID, self.path, self.isLoaded)
        
        
def getLoadedFrameworks():
    blist = []
    for i in NSBundle.allFrameworks():
        if i.isLoaded():
            blist += [Framework(i)]
    return blist
    
    
def getBundleWithID(bid):
    return Framework(NSBundle.bundleWithIdentifier_(bid))
    
    
def bundleForObjcClass(objc):
    return Framework(NSBundle.bundleForClass_(objc))
    

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
    return Framework(NSBundle.bundleWithPath_(path))
