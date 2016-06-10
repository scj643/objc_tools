from objc_util import ObjCClass
UIApplication = ObjCClass('UIApplication')
a = UIApplication.sharedApplication()


def stopRecivingTouch():
    # Will make the app stop responding to touch
    a.setIgnoresInteractionEvents_(True)


def startRecivingTouch():
    a.setIgnoresInteractionEvents_(False)
    

def setBadgeString(bstring):
    # set's Pythonista's app badge to a string instead of a number
    if type(bstring) == str:
        a.setApplicationBadgeString_(bstring)
        return True
    else:
        return False
    
def backgroundTimeRemaining():
    bgtime = a.backgroundTimeRemaining()
    if bgtime > 10000000:
        return None
    else:
        return bgtime
        


