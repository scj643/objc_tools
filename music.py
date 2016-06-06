from objc_util import ObjCClass, NSBundle, uiimage_to_png
from io import BytesIO
from PIL import Image
NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
MPMediaQuery = ObjCClass('MPMediaQuery')
MPMusicPlayerController = ObjCClass('MPMusicPlayerController')
MPMusicPlayerClientState = ObjCClass('MPMusicPlayerClientState')
#MPMediaPredicate = ObjCClass('MPMediaPredicate')
#MPMediaPropertyPredicate = ObjCClass('MPMediaPropertyPredicate')
musicapp = MPMusicPlayerController.systemMusicPlayer()

class song (object):
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
        
        
def nowplaying():
    np=musicapp.nowPlayingItem()
    if np:
        return song(np)

def playback_status():
    status = musicapp.playbackState()
    if status == 0:
        return 'Not Running'
    if status == 1:
        return 'Playing'
    if status == 2:
        return 'Paused'

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
    status = musicapp.playbackState()
    if status == 1:
        musicapp.pause()
    else:
        musicapp.play()
    
def stop():
    musicapp.stop()

def skip():
    musicapp.setCurrentPlaybackTime_(99999)
    
    
def next_song_info():
    return song(musicapp.nowPlayingItemAtIndex_(musicapp.indexOfNowPlayingItem()+1))


def library():
    query = MPMediaQuery.songsQuery()
    mlibrary = []
    for item in query.items():
        mlibrary += [song(item)]
    return mlibrary
    

def refresh_libs():
    MPMediaQuery = ObjCClass('MPMediaQuery')
    MPMusicPlayerController = ObjCClass('MPMusicPlayerController')
    MPMusicPlayerClientState = ObjCClass('MPMusicPlayerClientState')
    #MPMediaPredicate = ObjCClass('MPMediaPredicate')
    #MPMediaPropertyPredicate = ObjCClass('MPMediaPropertyPredicate')
    musicapp = MPMusicPlayerController.systemMusicPlayer()
    appmusicapp = MPMusicPlayerController.applicationMusicPlayer()
    
s=nowplaying()
