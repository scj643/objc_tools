from objc_util import ObjCClass, NSBundle, uiimage_to_png, nsurl, ObjCInstance, ns
from io import BytesIO
from PIL import Image
from urllib.parse import urlparse
from objc_tools.device import osVersion
from objc_tools.backports.enum_backport import IntEnum, Flag
from objc_tools.foundation.error import ObjcErrorHandler
media_player_bundle = NSBundle.bundleWithPath_('/System/Library/Frameworks'
                                               '/MediaPlayer.framework')
media_player_bundle.load()
iOS_version = osVersion()[0]+(osVersion()[1]/10)
del media_player_bundle, osVersion
MPMediaLibrary = ObjCClass("MPMediaLibrary")
MPMediaQuery = ObjCClass('MPMediaQuery')
MPMusicPlayerController = ObjCClass('MPMusicPlayerController')
file_handler = ObjCClass('AVAudioFile').alloc()

MPMediaPropertyPredicate = ObjCClass("MPMediaPropertyPredicate")
MPMediaItem = ObjCClass('MPMediaItem')


class RepeatMode (IntEnum):
    default = 0
    # We use lowercase none to seperate it from the keyword None
    none = 1
    one = 2
    all = 3
        

class ShuffleMode (IntEnum):
    default = 0
    off = 1
    songs = 2
    albums = 3
    

class PlaybackState (IntEnum):
    stoped = 0
    playing = 1
    paused = 2
    interrupted = 3
    seekingForward = 4
    seekingBackward = 5


class FileDesc (object):
    """Used to get information on a media file"""
    def __init__(self, url):
        if type(url) == str:
            url = nsurl(url)
        if type(url) == ObjCInstance:
            self.errorhandler = ObjcErrorHandler()
            self._objc = file_handler.initForReading_error_(url, None)
            fformat = self._objc.fileFormat()
            self.sampleRate = fformat.sampleRate()
            self.channels = fformat.channelCount()
            self.format = urlparse(str(url)).path.split('.')[-1]


class Song (object):
    """Parses song items
    :song: an objc instance of a song item
    """
    def __init__(self, song):
        try:
            song.title()
        except AttributeError:
            raise TypeError('Not a song item')
        self.title = str(song.title())
        self.genre = str(song.genre()).replace('\n', '')
        self.composer = str(song.composer())
        self.artist = str(song.artist())
        self.albumArtist = str(song.albumArtist())
        self.duration = float(song.playbackDuration())
        self.skips = int(song.skipCount())
        self.rating = int(song.rating())
        self.comments = str(song.comments())
        self.inLibrary = song.existsInLibrary()
        self.compolation = song.isCompilation()
        self.cloud = song.isCloudItem()
        if len(str(song.lyrics())):
            self.lyrics = str(song.lyrics())
        else:
            self.lyrics = None
        self.playCount = song.playCount()
        self.year = int(song.year())
        self.album = str(song.albumTitle())
        self.trackNumber = song.albumTrackNumber()
        self.discNumber = song.discNumber()
        if song.beatsPerMinute():
            self.bpm = song.beatsPerMinute()
        else:
            self.bpm = None
        self.assetURL = song.assetURL()
        self._objc = song

    def __str__(self):
        return '{0} - {1} - ({2})'.format(self.title, self.artist, self.album)
        
    def __repr__(self):
        return '<Song: {0} - {1} - ({2})>'.format(self.title, self.artist, self.album)
        
    def artwork(self, brep=False):
        """Get artwork for the song item
        brep determines if we want a PIL image or just the binary version
        """
        if self._objc.artworkCatalog():
            uiimage = self._objc.artworkCatalog().bestImageFromDisk()
            if brep:
                return uiimage_to_png(uiimage)
            else:
                i = BytesIO(uiimage_to_png(uiimage))
                return Image.open(i)
        else:
            return None
    
    def file_info(self):
        """Sets the file atribute of the item (used to save memory)"""
        self.file = FileDesc(self.assetURL)
    

class Playlist (object):
    """Playlist object"""
    def __init__(self, playlist):
        try:
            playlist.name()
        except AttributeError:
            raise TypeError('Not a playlist item')
        self.title = str(playlist.name())
        self.cloudMix = playlist.isCloudMix()
        self.inLibrary = playlist.existsInLibrary()
        if iOS_version >= 9.3:
            self.description = str(playlist.descriptionText())
            self.authorName = str(playlist.authorDisplayName())
        else:
            self.description = None
            self.authorName = None
        self.itemCount = playlist.count()
        self._objc = playlist
    
    class Attributes (Flag):
        AttributeNone = 0
        AttributeOnTheGo = (1 << 0)  # if set, the playlist was created on a device rather than synced from iTunes
        AttributeSmart = (1 << 1)
        AttributeGenius = (1 << 2)
    
    def __str__(self):
        return self.title
    
    def __repr__(self):
        return "<Playlist: {0}>".format(self.title)
    
    @property
    def attributes(self):
        return self.Attributes(self._objc.playlistAttributes())
    
    @property
    def songs(self):
        """Populate the items item"""
        returns = []
        for i in self._objc.items():
            returns += [Song(i)]
        return returns
    
    def artwork(self, brep=False):
        """Get artwork for the song item
        brep determines if we want a PIL image or just the binary version
        """
        if self._objc.artworkCatalog():
            uiimage = self._objc.artworkCatalog().bestImageFromDisk()
            if brep:
                return uiimage_to_png(uiimage)
            else:
                i = BytesIO(uiimage_to_png(uiimage))
                return Image.open(i)
        else:
            return None
            
    def setName(self, text):
        """Sets the name of the playlist
        Returns True or False if the name was changed or not
        """
        if type(text) != str:
            raise TypeError('Must be string')
        else:
            state = self._objc.setValue_forProperty_(text, 'name')
            if state:
                self.title = text
                return True
            else:
                return False
            
    # Too unstable to use
    """def artworkTile(self, brep=False, rows = 2, columns = 2):
        Get artwork for the song item
        brep determines if we want a PIL image or just the binary version
        
        finished = False
        if self.playlist.tiledArtworkCatalogWithRows_columns_(rows, columns).hasImageOnDisk():
            finished = True
        else:
            self.playlist.tiledArtworkCatalogWithRows_columns_(rows, columns).requestImageWithCompletionHandler(None)
            sleep(0.5)
        uiimage = self.playlist.tiledArtworkCatalogWithRows_columns_(rows, columns).bestImageFromDisk()
        if brep:
            return uiimage_to_png(uiimage)
        else:
            i = BytesIO(uiimage_to_png(uiimage))
            return Image.open(i)
"""

    def addSong(self, song):
        if isinstance(song, (Song)):
            if iOS_version >= 9.3:
                self._objc.addItem_completionBlock_(song._objc, None)
            else:
                raise OSError("Adding songs requires iOS 9.3 or greater")
        else:
            raise TypeError('Must be a song')


class Filter (object):
    """Used for filtering the media library
    
    query: The text to search
    ftype: a filter type. Must be one of the filter properties from https://developer.apple.com/reference/mediaplayer/mpmediaitem?language=objc
    contains: Bollean if set will check if it contains the query else it will look for exact matches.
    """
    def __init__(self, query, ftype, contains=True):
        if not canFilter(ftype):
            raise TypeError('ftype not filterable')
        else:
            self.query = [{'query': query, 'property': ftype, 'contains': contains}]
        
    def __repr__(self):
        returns = '<filter '
        for i in self.query:
            returns += '[Query: {0}, Property: {1}, Contains: {2}], '.format(i['query'], i['property'], i['contains'])
        returns = returns.rsplit(',', 1)[0]
        return returns+'>'
        
    def add(self, query, ftype, contains):
        if not canFilter(ftype):
            raise TypeError('ftype not filterable')
        else:
            self.query += [{'query': query, 'property': ftype, 'contains': contains}]
            
    def getMatches(self):
        query = MPMediaQuery.songsQuery()
        returns = []
        for i in self.query:
            query.addFilterPredicate_(MPMediaPropertyPredicate.predicateWithValue_forProperty_comparisonType_(i['query'], i['property'], int(i['contains'])))
        for i in query.items():
            returns += [Song(i)]
        return returns
        

class NowPlayingController (object):
    def __init__(self, _objc=MPMusicPlayerController.systemMusicPlayer()):
        self._objc = _objc
        self.error = None
        
    @property
    def repeat(self):
        return RepeatMode(self._objc.repeatMode())
    
    @repeat.setter
    def repeat(self, mode):
        """Set the music player repeat mode
           Must be an int or RepeatMode Object
        """
        self._objc.setRepeatMode_(int(mode))
        
    @property
    def shuffle(self):
        return ShuffleMode(self._objc.shuffleMode())
        
    @shuffle.setter
    def shuffle(self, mode):
        """Set the player's shuffle mode
           Must be a ShuffleMode item or an int
        """
        self._objc.setShuffleMode_(int(mode))
    
    @property
    def state(self):
        return PlaybackState(self._objc.playbackState())
        
    @property
    def now_playing(self):
        if self._objc.nowPlayingItem():
            return Song(self._objc.nowPlayingItem())
        else:
            return None
    
    @now_playing.setter
    def now_playing(self, item):
        if isinstance(item, Song):
            self._objc.setNowPlayingItem_(item._objc)

    def play(self):
        """Starts playback of the music app"""
        self._objc.play()
    
    def pause(self):
        """Pauses playback of the music app"""
        self._objc.pause()
        
    def play_pause(self):
        """Toggles playback state of the music app"""
        if self.state == PlaybackState.playing:
            self._objc.pause()
        else:
            self._objc.play()
    
    def stop(self):
        """Stops playback of the music app"""
        self._objc.stop()
    
    def skip_next(self):
        """Skips to the next song in the music app"""
        error = ObjcErrorHandler()
        self._objc.skipInDirection_error_(1, error)
        e = error.error()
        self.error = e
    
    def replay(self):
        """Returns to the begining of the current song"""
        self._objc.setCurrentPlaybackTime_(0)
    
    def skip_previous(self):
        error = ObjcErrorHandler()
        """Returns to the song before the current song in the music app"""
        self._objc.skipInDirection_error_(-1, error)
        e = error.error()
        self.error = e
    
    @property
    def next_song_info(self):
        """Returns the song instance of the next song to be played"""
        cur_index = self._objc.indexOfNowPlayingItem()
        return Song(self._objc.nowPlayingItemAtIndex_(cur_index+1))
    
    @property
    def volume(self):
        """Get's the current volume"""
        return self._objc.volume()
        
    @volume.setter
    def volume(self, v):
        """Officially unsupported method of changing the volume
        Must be a float from 0 to 1
        """
        if type(v) != float:
            if type(v) == int:
                v = float(v)
            else:
                raise TypeError('Has to be a number')
    
        if not 0 <= v <= 1:
            raise ValueError('Has to be between 0 or 1')
        
        self._objc.setVolume_(v)
        
    @property
    def playbackRate(self):
        return self._objc.currentPlaybackRate()
    
    @playbackRate.setter
    def playbackRate(self, rate):
        self._objc.setCurrentPlaybackRate_(rate)
        
    @property
    def playbackTime(self):
        return self._objc.currentPlaybackTime()
        
    @playbackTime.setter
    def playbackTime(self, time):
        self._objc.setCurrentPlaybackTime_(time)
        
    @property
    def items_amount(self):
        return self._objc.numberOfItems()
        
    @property
    def index_of_nowplaying(self):
        return self ._objc.indexOfNowPlayingItem()
        
    def song_at_index(self, index):
        while index > self.items_amount:
            # wrap around so we always get an item
            index -= self.items_amount
        return Song(self._objc.nowPlayingItemAtIndex_(index))

    def song_list(self):
        returns = []
        for i in range(self.items_amount):
            returns += [self.song_at_index(i)]
        return returns

def library():
    """Returns all the items in the music app's library"""
    query = MPMediaQuery.songsQuery()
    mlibrary = []
    for item in query.items():
        mlibrary += [Song(item)]
    return mlibrary
    

def playlists():
    returns = []
    if len(MPMediaQuery.playlistsQuery().collections()) < 1:
        raise ValueError("No Playlists")
        return []
    for i in MPMediaQuery.playlistsQuery().collections():
        returns += [Playlist(i)]
    return returns


def auth_status():
    if iOS_version < 9.3:
        raise OSError("Not needed before iOS 9.3")
        return True
    else:
        status = MPMediaLibrary.authorizationStatus()
        
        class AuthStatus (IntEnum):
            Unknown = 0
            Denied = 1
            Restricted = 2
            Authorized = 3
        return AuthStatus(status)
            

def canFilter(key):
    return MPMediaItem.canFilterByProperty_(key)
    

def songlist_to_array(songs):
    objcitems = []
    for i in songs:
        objcitems += [i._objc]
    return ns(objcitems)
    
if __name__ == '__main__':
    p = playlists()[0]
    n = NowPlayingController()
