from objc_util import ObjCClass, load_framework, nsurl, ObjCInstance, type_encodings
from objc_tools.objchandler import urlHandle
from objc_tools.core.media import CMTime
import ui

load_framework('AVFoundation')
load_framework('AVKit')


AVPlayerViewController = ObjCClass('AVPlayerViewController')
AVAsset = ObjCClass('AVAsset')
AVPlayerLayer = ObjCClass('AVPlayerLayer')
AVPlayerItem = ObjCClass('AVPlayerItem')
AVPlayer = ObjCClass('AVPlayer')
AVTimeFormatter = ObjCClass('AVTimeFormatter')

class Asset (object):
    '''Python class for AVAsset
    '''
    def __init__(self, url):
        path = urlHandle(url)
        self._objc = AVAsset.assetWithURL_(path)
        
    @property
    def isPlayable(self):
        return self._objc.isPlayable()
    
    @isPlayable.setter
    def isPlayable(self, value):
        pass
        
    @property
    def isReadable(self):
        return self._objc.isReadable()
    
    @isReadable.setter
    def isReadable(self, value):
        pass


class PlayerItem (object):
    '''A player item that bridges AVPlayerItem
    Used with players
    '''
    def __init__(self, asset):
        if type(asset) == Asset:
            self._objc = AVPlayerItem.playerItemWithAsset_(asset._objc)
        else:
            raise TypeError
    
    
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
            self._objc = AVPlayer.playerWithPlayerItem_(setitem._objc)
            self._item = setitem
        else:
            raise TypeError
            
    def play(self):
        if self._objc:
            self._objc.play()
            
    def pause(self):
        if self._objc:
            self._objc.pause()
    
    
class PlayerView (ui.View):
    '''A player view with controls'''
    def __init__(self, player = None):
         self._objc = ObjCInstance(self)
         self._playerViewController = AVPlayerViewController.new()
         self._objc.addSubview_(self._playerViewController.view())
         self.player = player
    @property
    def player(self):
        return self._playerItem
     
    @player.setter
    def player(self, player):
        if type(player) == Player:
            self._playerItem = player
            self._playerViewController = self._playerViewController.setPlayer_(player._objc)
        else:
            raise TypeError
             

