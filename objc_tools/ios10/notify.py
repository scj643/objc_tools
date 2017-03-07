from objc_util import *
from objc_tools.backports.enum_backport import IntEnum
from objc_tools import blocks
load_framework('UserNotifications')


def handler(_cmd, *args):
    global objects
    objects = []
    for i in args:
        objects += [ObjCInstance(i)]
    
    
UNNotification = ObjCClass('UNNotification')
UNNotificationSettings = ObjCClass('UNNotificationSettings')
UNUserNotificationCenter = ObjCClass('UNUserNotificationCenter')
UNMutableNotificationContent = ObjCClass('UNMutableNotificationContent')
UNTimeIntervalNotificationTrigger = ObjCClass('UNTimeIntervalNotificationTrigger')
UNNotificationRequest = ObjCClass('UNNotificationRequest')

class UNAuthorizationStatus(IntEnum):
    #The user has not yet made a choice regarding whether the application may post user notifications.
    UNAuthorizationStatusNotDetermined = 0
    
    #The application is not authorized to post user notifications.
    UNAuthorizationStatusDenied = 1
    
    #The application is authorized to post user notifications.
    UNAuthorizationStatusAuthorized = 2
    
    
    
class Settings (object):
        
    def get_settings(self):
        b = blocks.Block()
        self.c=UNUserNotificationCenter.currentNotificationCenter()
        c.getNotificationSettingsWithCompletionHandler_(b)

if __name__ == '__main__':
    c=UNUserNotificationCenter.currentNotificationCenter()
    n = UNMutableNotificationContent.alloc()
    n.title = 'test'
    n.body = 'test'
    trigger = UNTimeIntervalNotificationTrigger.triggerWithTimeInterval_repeats_(5, False)
    req = UNNotificationRequest.requestWithIdentifier_content_trigger_('test', n, trigger)
    b = blocks.Block()
    id = c.getNotificationSettingsWithCompletionHandler_(b.block)
    c.addNotificationRequest_(req)
