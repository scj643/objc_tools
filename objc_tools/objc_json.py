from objc_util import ObjCClass, nsdata_to_bytes
import json

NSJSONSerialization = ObjCClass('NSJSONSerialization')

def checkObject(objc):
    return NSJSONSerialization.isValidJSONObject_(objc)
    

def objc_to_str(objc, pretty=True):
    if checkObject(objc):
        return nsdata_to_bytes(NSJSONSerialization.dataWithJSONObject_options_error_(objc, int(pretty), None)).decode('utf-8')
    else:
        raise TypeError("Objc object can't be converted")
        return None
    

def objc_to_py(objc):
    if checkObject(objc):
        return json.loads(objc_to_str(objc))
    else:
        raise TypeError("Objc object can't be converted")
        return None
