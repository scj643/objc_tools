from objc_util import c_void_p, ObjCInstance
from objc_tools.objc_json import objc_to_py


class LocalizedStrings (object):
    def __init__(self, objc):
        self.recovery_suggestion = str(objc.localizedRecoverySuggestion())
        self.failureReason = str(objc.localizedFailureReason())
        self.recovery_options = str(objc.localizedRecoveryOptions())
        self.description = str(objc.localizedDescription())


class NSError (object):
    def __init__(self, objc):
        self._objc = objc
        self.descriptions = LocalizedStrings(self._objc)
        self.info = objc_to_py(self._objc.userInfo())
        self.domain = str(self._objc.domain())
        self.code = self._objc.code()
        
    def __repr__(self):
        return '<NSError: Description: "{}">'.format(self.descriptions.description)
        

class ObjcErrorHandler (c_void_p):
    '''ObjcErrorHandler Used as a pointer to an error
       Must be set first then used
       >>> pointer = ObjcErrorHandler()
       >>> result = someObjcBridgeFunctionWithError_(pointer)
       >>> error = pointer.error()
    '''
    def error(self):
        if self.value:
            return NSError(ObjCInstance(self))
