from objc_util import ObjCClass
reachablity = ObjCClass('IMNetworkReachability')
manager = ObjCClass('IMDesktopNetworkManager')
monitor = ObjCClass('IMConnectionMonitor')
IMPingTest = ObjCClass('IMPingTest')

def is_online():
    return bool(reachablity.reachabilityForInternetConnection().currentReachabilityStatus())
    

def is_airplane_mode():
    return manager.sharedInstance().isAirplaneModeEnabled()


def ping(address, rounds=3):
    '''returns a IMPingTest object'''
    p = IMPingTest.new().initWithAddress_wifi_(address, None)
    p.startWithTimeout_queue_completionHandler_(rounds ,None, None)
    return p
    
    
g
