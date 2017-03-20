from objc_util import ObjCClass, load_framework, nsurl, ObjCInstance, CGRect, CGPoint, CGSize
from objc_tools.objchandler import urlHandle
from objc_tools.core.media import CMTime, CMTimeMakeWithSeconds
import ui
from objc_tools.backports.enum_backport import IntEnum, Enum
load_framework('AVFoundation')
load_framework('AVKit')


class PlayerStatus (IntEnum):
    AVPLAYERSTATUSUNKNOWN = 0
    AVPLAYERSTATUSREADYTOPLAY = 1
    AVPLAYERSTATUSFAILED = 2


LAYER_RESIZE_MODES = ["AVLayerVideoGravityResizeAspect", "AVLayerVideoGravityResizeAspectFill", "AVLayerVideoGravityResize"]


AVPlayerViewController = ObjCClass('AVPlayerViewController')
AVAsset = ObjCClass('AVAsset')
AVPlayerLayer = ObjCClass('AVPlayerLayer')
AVPlayerItem = ObjCClass('AVPlayerItem')
AVPlayer = ObjCClass('AVPlayer')
AVTimeFormatter = ObjCClass('AVTimeFormatter')


class Asset (object):
    '''Python class for AVAsset
    url: a url to initialize
    objc_item: pass a AVAsset objc item
    '''
    def __init__(self, url = None, objc_item = None):
        if url:
            path = urlHandle(url)
        else:
            path = None
            
        if path:
            self._objc = AVAsset.assetWithURL_(path)
        
        if objc_item:
            self._objc = objc_item

    @property
    def isPlayable(self):
        return self._objc.isPlayable()

    @property
    def isReadable(self):
        return self._objc.isReadable()
        
    @property
    def url(self):
        return str(self._objc.URL().absoluteString())
        
    def __repr__(self):
        return '<Asset <URL: {}>>'.format(self.url)



class PlayerItem (object):
    '''A player item that bridges AVPlayerItem
    Used with players
    '''
    def __init__(self, asset=None, objc_item=None):
        if type(asset) == Asset:
            self._objc = AVPlayerItem.playerItemWithAsset_(asset._objc)
            self._asset = asset
        else:
            self._objc = None
        if objc_item:
            if objc_item.isKindOfClass(AVAsset):
                self._asset = Asset(objc_item=objc_item)
                self._objc = AVPlayerItem.playerItemWithAsset_(self._asset._objc)
            elif objc_item.isKindOfClass(AVPlayerItem):
                self._asset = Asset(objc_item=objc_item.asset())
                self._objc = AVPlayerItem.playerItemWithAsset_(self._asset._objc)
            else:
                raise TypeError('Not a compatable ObjC Asset')

    @property
    def volumeAdjustment(self):
        return self._objc.volumeAdjustment()

    @volumeAdjustment.setter
    def volumeAdjustment(self, volume):
        self._objc.volumeAdjustment = volume

    @property
    def status(self):
        return PlayerStatus(self._objc.status())
        
    @property
    def asset(self):
        return self._asset
        

class Player (object):
    '''A player item that is passed to player views
    Bridges with AVPlayer
    Uses a PlayerItem
    '''
    def __init__(self, playerItem):
        self._objc = None
        self.item = playerItem

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, setitem):
        if type(setitem) == PlayerItem:
            self._item = setitem
            if not self._objc:
                self._objc = AVPlayer.playerWithPlayerItem_(setitem._objc)
            else:
                self._objc.replaceCurrentItemWithPlayerItem_(setitem._objc)
        elif type(setitem) == ObjCInstance:
            if setitem.isKindOfClass(AVAsset):
                self._item = PlayerItem(objc_item = setitem)
                if not self._objc:
                    self._objc = AVPlayer.playerWithPlayerItem_(self._item._objc)
                else:
                    self._objc.replaceCurrentItemWithPlayerItem_(self._item._objc)
            else: raise TypeError('must be an AVAsset ObjC class')
        else:
            raise TypeError("must be a PlayerItem or ObjCInstance")

    def play(self):
        if self._objc:
            self._objc.play()

    def pause(self):
        if self._objc:
            self._objc.pause()

    @property
    def currentTime(self):
        if self._objc:
            return self._objc.currentTime(restype=CMTime, argtypes=[])

    @currentTime.setter
    def currentTime(self, time):
        '''Time is either a CMTime object or a tuple with a time, minetime, and max'''
        if self._objc:
            if type(time) == CMTime:
                self._objc.seekToTime_(time, argtypes=[CMTime], restype=None)
            if type(time) == list:
                self._objc.seekToTime_toleranceBefore_toleranceAfter_(time[0], time[1], time[2], argtypes=[CMTime, CMTime, CMTime], restype=None)
        
    @property
    def rate(self):
        if self._objc:
            return self._objc.rate()
            
    @rate.setter
    def rate(self, r):
        if self._objc:
            self._objc.setRate_(r)


class PlayerController (object):
    '''A player controller
    Used with player views
    '''
    def __init__(self, controller = None):
        self._objc = controller
        
    def seekToBegining(self):
        '''Seek to the controller begining
        returns true if it can otherwise false
        '''
        if self._objc.canSeekToBeginning():
            self._objc.seekToBeginning_(None)
            return True
        else:
            return False
            
    @property
    def frameRate(self):
        return self._objc.nominalFrameRate()
    
    @property
    def looping(self):
        return self._objc.isLooping()
        
    @looping.setter
    def looping(self, s):
        self._objc.setLooping_(s)
        
    def seekToTime(self, time):
        if type(time) in [int, float]:
            self._objc.seekToTime_(time)
        else:
            raise TypeError('Time is not a valid number')
    
    def seekFramesForward(self, frames=1):
        for i in frames:
            self._objc.seekFrameForward_(None)
            
    def seekFramesBackward(self, frames=1):
        for i in frames:
            self._objc.seekFrameBackward_(None)


class PlayerView (ui.View):
    '''A player view with controls'''
    def __init__(self, player = None, pause= True, autoplay = False, pip = False):
        self._pause_on_dismiss = pause
        self._objc = ObjCInstance(self)
        self._playerViewController = AVPlayerViewController.new()
        self._objc.addSubview_(self._playerViewController.view())
        self.player = player
        self._autoplay = autoplay
        self._playerViewController.setAllowsPictureInPicturePlayback_(pip)
        
    @property
    def player(self):
        return self._playerItem

    @player.setter
    def player(self, player):
        if type(player) == Player:
            self._playerViewController.setPlayer_(player._objc)
            self._playerItem = player
            self.controller = PlayerController(self._playerViewController.playerController())
        elif type(player) == type(None):
            self._playerViewController.setPlayer_(player)
            self._playerItem = None
        elif type(player) == ObjCInstance:
            self._playerItem = Player(player.currentItem())
            self._playerViewController.setPlayer_(self._playerItem)
            self.controller = PlayerController(self._playerViewController.playerController())
        else:
            raise TypeError("player is not able to be set")

    @player.deleter
    def player(self):
        self._playerViewController.setPlayer_(None)

    def will_close(self):
        if self._pause_on_dismiss:
            self.player.pause()

    def did_load(self):
        if self._autoplay:
            self.player.play()
            
    def layout(self):
        pass
        
    @property
    def pipSupported(self):
        self._playerViewController.allowsPictureInPicturePlayback()
        
    @pipSupported.setter
    def pipSupported(self, value):
        self._playerViewController.setAllowsPictureInPicturePlayback_(value)
        
    @property
    def showsPlaybackControls(self):
        return self._playerViewController.showsPlaybackControls()
        
    @showsPlaybackControls.setter
    def showsPlaybackControls(self, state):
        self._playerViewController.setShowsPlaybackControls_(state)
        
    
class PlayerLayerView (ui.View):
    def __init__(self,player, *args, **kwargs):
        ui.View.__init__(self,*args,**kwargs)
        if type(player) == Player:
            self._layer = AVPlayerLayer.playerLayerWithPlayer_(player._objc)
            self.player = player
        else:
            raise TypeError('Must be a Player item')
        self._layer.setVideoGravity_(
         'AVLayerVideoGravityResizeAspect')
        self._rootLayer=ObjCInstance(self).layer()
        self._rootLayer.setMasksToBounds_(True)
        self._layer.setFrame_(
         CGRect(CGPoint(0, 0), CGSize(self.width ,self.height)))
        self._rootLayer.insertSublayer_atIndex_(self._layer,0)
        
    @property
    def layerResizeMode(self):
        return self._layer.videoGravity()
        
    @layerResizeMode.setter
    def layerResizeMode(self, mode):
        if mode in LAYER_RESIZE_MODES:
            self._layer.setVideoGravity_(mode)
        else:
            raise TypeError('{} is not a valid mode'.format(mode))
        
    def layout(self):
        self._layer.setFrame_(
         CGRect(CGPoint(0, 0), CGSize(self.width, self.height)))

