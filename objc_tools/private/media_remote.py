from objc_util import c_void_p, c_int, c, c_bool, ObjCInstance, NSString, NSDictionary, c_char_p, ObjCClass
from objc_util import *
from objc_tools.backports.enum_backport import Enum
from objc_tools import blocks

global nowplaying
nowplaying = None

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
    
    
OMMainThreadDispatcher = ObjCClass('OMMainThreadDispatcher_3')

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
    
    


queue = q
MRMediaRemoteGetNowPlayingInfo = c.MRMediaRemoteGetNowPlayingInfo
MRMediaRemoteGetNowPlayingInfo.argtypes = [c_void_p, ObjCBlock]
#MRMediaRemoteGetNowPlayingInfo.restype =
#(queue, handler.ptr)
#return handler

t=NSThread.mainThread()

def bhandle(_cmd, d):
    global  nowplaying
    nowplaying = ObjCInstance(d)

handler = ObjCBlock(bhandle, argtypes=[c_void_p, c_void_p])

def set_route(route, pw):
    MRMediaRemoteSetPickedRouteWithPassword = c.MRMediaRemoteSetPickedRouteWithPassword
    MRMediaRemoteSetPickedRouteWithPassword.argtypes=[c_void_p, c_void_p]
    MRMediaRemoteSetPickedRouteWithPassword(ns(route).ptr, ns(pw).ptr)
