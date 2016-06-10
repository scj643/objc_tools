from objc_util import ObjCClass, NSBundle, uiimage_to_png, nsurl, ObjCInstance
from io import BytesIO
from PIL import Image
from urllib.parse import urlparse
NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
MPMediaQuery = ObjCClass('MPMediaQuery')
MPMusicPlayerController = ObjCClass('MPMusicPlayerController')
file_handler = ObjCClass('AVAudioFile').alloc()
#MPMediaPredicate = ObjCClass('MPMediaPredicate')
#MPMediaPropertyPredicate = ObjCClass('MPMediaPropertyPredicate')
musicapp = MPMusicPlayerController.systemMusicPlayer()

class FileDesc (object):
    def __init__(self, url):
        if type(url) == str:
            url = nsurl(url)
        if type(url) == ObjCInstance:
            sf = file_handler.initForReading_error_(url, None)
            fformat = sf.fileFormat()
            self.sampleRate = fformat.sampleRate()
            self.channels = fformat.channelCount()
            self.format = urlparse(str(url)).path.split('.')[-1]

class Song (object):
    def __init__(self, song):
        try:
            song.title()
        except AttributeError:
            raise TypeError('Not a song item')
        self.title = str(song.title())
        self.genre = str(song.genre()).replace('\n','')
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
        return '{0} - {1} - ({2})'.format(self.title, self.artist, self.album)
        
    def artwork(self, brep=False):
        if self.song.artworkCatalog():
            if brep:
                return uiimage_to_png(self.song.artworkCatalog().bestImageFromDisk())
            else:
                i=BytesIO(uiimage_to_png(self.song.artworkCatalog().bestImageFromDisk()))
                return Image.open(i)
        else:
            return None
    
    def file_info(self):
        self.file=FileDesc(self.assetURL)
    
    def save(self, location):
        sf = file_handler.initForReading_error_(self.assetURL, None)
        
        

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
    if mode == 'Default':
        musicapp.setShuffleMode_(0)
    if mode == 'Off':
        musicapp.setShuffleMode_(1)
    if mode == 'Songs':
        musicapp.setShuffleMode_(2)
    if mode == 'Albums':
        musicapp.setShuffleMode_(3)

def playback_status():
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
    np=musicapp.nowPlayingItem()
    if np:
        return Song(np)

def play():
    musicapp.play()

def pause():
    musicapp.pause()

def set_volume(v):
    if type(v) != float:
        if type(v) == int:
            v = float(v)
        else:
            raise TypeError('Has to be a number')

    if not 0<= v <= 1:
        raise ValueError('Has to be between 0 or 1')
    
    musicapp.setVolume_(v)

def get_volume():
    return musicapp.volume()
    
def ptoggle():
    status = playback_status()
    if status == 'Playing':
        musicapp.pause()
    else:
        musicapp.play()
    
def stop():
    musicapp.stop()


def skip_next():
    musicapp.skipInDirection_error_(1, None)


def replay():
    musicapp.setCurrentPlaybackTime_(0)
    

def skip_previous():
    musicapp.skipInDirection_error_(-1, None)
    

def next_song_info():
    return Song(musicapp.nowPlayingItemAtIndex_(musicapp.indexOfNowPlayingItem()+1))


def library():
    query = MPMediaQuery.songsQuery()
    mlibrary = []
    for item in query.items():
        mlibrary += [Song(item)]
    return mlibrary
    

