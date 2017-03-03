from objc_util import ObjCClass, NSBundle, uiimage_to_png, nsurl, ObjCInstance
from io import BytesIO
from PIL import Image
urlprase = None
try:
    from urllib.prase import urlprase
except ImportError:
    import urllib2
    urlprase = urllib2.urlparse
from objc_tools.device import osVersion
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


musicapp = MPMusicPlayerController.systemMusicPlayer()


class FileDesc (object):
    """Used to get information on a media file"""
    def __init__(self, url):
        if type(url) == str:
            url = nsurl(url)
        if type(url) == ObjCInstance:
            self.sf = file_handler.initForReading_error_(url, None)
            fformat = self.sf.fileFormat()
            self.sampleRate = fformat.sampleRate()
            self.channels = fformat.channelCount()
            self.format = urlparse(str(url)).path.split('.')[-1]


class Song (object):
    """Parses song items"""
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
        self.song = song

    def __str__(self):
        return '{0} - {1} - ({2})'.format(self.title, self.artist, self.album)
        
    def __repr__(self):
        return '<Song: {0} - {1} - ({2})>'.format(self.title, self.artist, self.album)
        
    def artwork(self, brep=False):
        """Get artwork for the song item
        brep determines if we want a PIL image or just the binary version
        """
        if self.song.artworkCatalog():
            uiimage = self.song.artworkCatalog().bestImageFromDisk()
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
        self.items = []
        self.cloudMix = playlist.isCloudMix()
        self.inLibrary = playlist.existsInLibrary()
        self.artists = []
        if playlist.representativeArtists():
            for i in playlist.representativeArtists():
                self.artists += [i]
        self.description = str(playlist.descriptionText())
        self.itemCount = playlist.count()
        self.playlist = playlist
    
    
    def __str__(self):
        return self.title
    
    
    def __repr__(self):
        return "<Playlist: {0}>".format(self.title)
        
    
    def getSongs(self):
        """Populate the items item"""
        for i in self.playlist.items():
            self.items += [Song(i)]
    
    
    def artwork(self, brep=False):
        """Get artwork for the song item
        brep determines if we want a PIL image or just the binary version
        """
        if self.playlist.artworkCatalog():
            uiimage = self.playlist.artworkCatalog().bestImageFromDisk()
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
            state = self.playlist.setValue_forProperty_(text,'name')
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
        if type(song) == Song:
            if iOS_version > 9.3:
                self.playlist.addItem_completionBlock_(song.song, None)
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
        returns = returns.rsplit(',',1)[0]
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
        
        
def repeat_mode():
    status = musicapp.repeatMode()
    if status == 0:
        return 'Default'
    if status == 1:
        return 'None'
    if status == 2:
        return 'One'
    if status == 3:
        return 'All'
        

def set_repeat_mode(mode):
    """Set the music player repeat mode
    Can be 'Default', 'None', 'One', or 'All'
    """
    if mode == 'Default':
        musicapp.setRepeatMode_(0)
    if mode == 'None':
        musicapp.setRepeatMode_(1)
    if mode == 'One':
        musicapp.setRepeatMode_(2)
    if mode == 'All':
        musicapp.setRepeatMode_(3)

                
def shuffle_mode():
    status = musicapp.shuffleMode()
    if status == 0:
        return 'Default'
    if status == 1:
        return 'Off'
    if status == 2:
        return 'Songs'
    if status == 3:
        return 'Albums'

                
def set_shuffle_mode(mode):
    """Set the music player shuffel mode
    Can be 'Default', 'Off', 'Songs', or 'Albums'
    """
    if mode == 'Default':
        musicapp.setShuffleMode_(0)
    if mode == 'Off':
        musicapp.setShuffleMode_(1)
    if mode == 'Songs':
        musicapp.setShuffleMode_(2)
    if mode == 'Albums':
        musicapp.setShuffleMode_(3)


def playback_status():
    """Gets the current playback state
    Returned as a human readable string
    """
    status = musicapp.playbackState()
    if status == 0:
        return 'Stopped'
    if status == 1:
        return 'Playing'
    if status == 2:
        return 'Paused'
    if status == 3:
        return 'Interrupted'
    if status == 4:
        return 'SeekingForward'
    if status == 5:
        return 'SeekingBackward'
        

def nowplaying():
    """Returns the now playing song as a Song item"""
    np = musicapp.nowPlayingItem()
    if np:
        return Song(np)


def play():
    """Starts playback of the music app"""
    musicapp.play()


def pause():
    """Pauses playback of the music app"""
    musicapp.pause()


def set_volume(v):
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
    
    musicapp.setVolume_(v)


def get_volume():
    """Get's the current volume"""
    return musicapp.volume()


def ptoggle():
    """Toggles playback state of the music app"""
    status = playback_status()
    if status == 'Playing':
        musicapp.pause()
    else:
        musicapp.play()

        
def stop():
    """Stops playback of the music app"""
    musicapp.stop()


def skip_next():
    """Skips to the next song in the music app"""
    musicapp.skipInDirection_error_(1, None)


def replay():
    """Returns to the begining of the current song"""
    musicapp.setCurrentPlaybackTime_(0)
    

def skip_previous():
    """Returns to the song before the current song in the music app"""
    musicapp.skipInDirection_error_(-1, None)
    

def next_song_info():
    """Returns the song instance of the next song to be played"""
    cur_index = musicapp.indexOfNowPlayingItem()
    return Song(musicapp.nowPlayingItemAtIndex_(cur_index+1))


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


def authStatus():
    if iOS_version < 9.3:
        raise OSError("Not needed before iOS 9.3")
        return True
    else:
        status = MPMediaLibrary.authorizationStatus()
        if status == 3:
            return 'Authorized'
        if status == 1:
            return 'Denied'
        if status == 0:
            return 'Unkown'
        if status == 2:
            return 'Restricted'
            

def canFilter(key):
    return MPMediaItem.canFilterByProperty_(key)
