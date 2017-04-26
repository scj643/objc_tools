from objc_util import ObjCClass
from objc_tools.backports.enum_backport import Flag, IntEnum
UIApplication = ObjCClass('UIApplication')

class UIUserNotificationType (Flag):
    UIUserNotificationTypeNone = 0 # the application may not present any UI upon a notification being received
    UIUserNotificationTypeBadge = 1 << 0 # the application may badge its icon upon a notification being received
    UIUserNotificationTypeSound = 1 << 1 # the application may play a sound upon a notification being received
    UIUserNotificationTypeAlert = 1 << 2 # the application may display an alert upon a notification being received
    
            
class UIBackgroundRefreshStatus (IntEnum):
    UIBackgroundRefreshStatusRestricted = 0
    UIBackgroundRefreshStatusDenied = 1
    UIBackgroundRefreshStatusAvailable = 2


class UIApplicationState (IntEnum):
    UIApplicationStateActive = 0
    UIApplicationStateInactive = 1
    UIApplicationStateBackground = 2
    
    
class UIApp (object):
    def __init__(self):
        '''A class for managing properties of the running app.'''
        self._objc = UIApplication.sharedApplication()
        
    
    @property    
    def reciving_touch(self):
        '''The state of the app weither or not to respond to touch
           return: A boolean state'''
        return not self._objc.ignoresInteractionEvents()
    
    @reciving_touch.setter
    def reciving_touch(self, state):
        self._objc.setIgnoresInteractionEvents_(not state)
    
    
    def setBadgeString(self, bstring):
        # set's Pythonista's app badge to a string instead of a number
        if type(bstring) == str:
            self._objc.setApplicationBadgeString_(bstring)
            return True
        else:
            return False
        
    @property
    def background_time_remaining(self):
        '''Get the remaining background time
           Not setable'''
        bgtime = self._objc.backgroundTimeRemaining()
        if bgtime > 10000000:
            return -1
        else:
            return bgtime
    
    
    @property
    def background_refresh_status(self):
        return UIBackgroundRefreshStatus(self._objc.backgroundRefreshStatus())
        
    
    @property
    def badge_number(self):
        return self._objc.applicationIconBadgeNumber()
    
    @badge_number.setter
    def badge_number(self, num):
        self._objc.setApplicationIconBadgeNumber_(num)
        
    @property
    def state(self):
        return UIApplicationState(self._objc.applicationState())
        
    @property
    def notification_settings(self):
        return UIUserNotificationType(self._objc.currentUserNotificationSettings().allowedUserNotificationTypes())
        
    @property
    def registered_for_remote_notifications(self):
        return self._objc.isRegisteredForRemoteNotifications()
        

class RootView (object):
    def __init__(self):
        self._objc = UIApplication.sharedApplication().keyWindow().rootViewController().view()
        for i in self._objc.gestureRecognizers():
            if b'UIPanGestureRecognizer' == i._get_objc_classname():
                self._slide_gesture = i
        
    @property
    def sliding_gesture_enabled(self):
        return self._slide_gesture.isEnabled()
        
    @sliding_gesture_enabled
    def sliding_gesture_enabled(self, value):
        self._slide_gesture.setEnabled_(value)

if __name__ == '__main__':
    p = UIApp()
    o = p._objc
