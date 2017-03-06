from objc_util import c_void_p, c_int, c, c_bool, ObjCInstance, NSString, ObjCBlock, c_char_p, ObjCClass, c_long, c_ulong
from objc_tools.backports.enum_backport import Enum
from sys import modules

global nowplaying

class Commands (Enum):
    kMRPlay = 0
    kMRPause = 1
    kMRTogglePlayPause = 2
    kMRStop = 3
    kMRNextTrack = 4
    kMRPreviousTrack = 5
    kMRToggleShuffle = 6
    kMRToggleRepeat = 7
    kMRStartForwardSeek = 8
    kMREndForwardSeek = 9
    kMRStartBackwardSeek = 10
    kMREndBackwardSeek = 11
    kMRGoBackFifteenSeconds = 12
    kMRSkipFifteenSeconds = 13
    

MRMediaRemoteGetNowPlayingInfo = c.MRMediaRemoteGetNowPlayingInfo
MRMediaRemoteGetNowPlayingInfo.argtypes = [c_void_p, ObjCBlock]

MRMediaRemoteSendCommand = c.MRMediaRemoteSendCommand
MRMediaRemoteSendCommand.argtypes = [c_int, c_void_p]
MRMediaRemoteSendCommand.restype = c_bool

dispatch_get_global_queue = c.dispatch_get_global_queue
dispatch_get_global_queue.argtypes = [c_long, c_ulong]
dispatch_get_global_queue.restype = c_void_p

q=dispatch_get_global_queue(0, 0)

def routes():
    MRMediaRemoteCopyPickableRoutes = c.MRMediaRemoteCopyPickableRoutes
    MRMediaRemoteCopyPickableRoutes.argtypes = []
    MRMediaRemoteCopyPickableRoutes.restype = c_void_p
    return ObjCInstance(MRMediaRemoteCopyPickableRoutes())

def route_has_volume_control():
    MRMediaRemotePickedRouteHasVolumeControl = c.MRMediaRemotePickedRouteHasVolumeControl
    MRMediaRemotePickedRouteHasVolumeControl.argtypes = []
    MRMediaRemotePickedRouteHasVolumeControl.restype = c_bool
    return MRMediaRemotePickedRouteHasVolumeControl()
    

class Nowplaying (object):
    def __init__(self):
        self.nowplaying = None
    
    def get(self, block = True):
        #handler = ObjCBlock(handle, argtypes=[c_void_p, c_void_p])
        MRMediaRemoteGetNowPlayingInfo(queue, handler)
        this = modules[__name__]
        
        if block:
            this.nowplaying = None
            while not this.nowplaying:
                pass
            self.nowplaying = this.nowplaying
            this.nowplaying = None
        else:
            self.nowplaying = this.nowplaying
            this.nowplaying = None
        


def bhandle(_cmd, d):
        global  nowplaying
        nowplaying = ObjCInstance(d)
        
        
queue = dispatch_get_global_queue(0, 0)
MRMediaRemoteGetNowPlayingInfo = c.MRMediaRemoteGetNowPlayingInfo
MRMediaRemoteGetNowPlayingInfo.argtypes = [c_void_p, ObjCBlock]
handler = ObjCBlock(bhandle, argtypes=[c_void_p, c_void_p])

def get():
    MRMediaRemoteGetNowPlayingInfo(queue, handler)

def set_route(route, pw):
    MRMediaRemoteSetPickedRouteWithPassword = c.MRMediaRemoteSetPickedRouteWithPassword
    MRMediaRemoteSetPickedRouteWithPassword.argtypes=[c_void_p, c_void_p]
    MRMediaRemoteSetPickedRouteWithPassword(ns(route).ptr, ns(pw).ptr)
    
n=Nowplaying()
n.get()

