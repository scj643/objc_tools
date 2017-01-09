from objc_util import ObjCClass, nsurl, ObjCInstance, UIImage, uiimage_to_png
from datetime import datetime
from io import BytesIO
from PIL import Image

LSApplicationWorkspace = ObjCClass('LSApplicationWorkspace')
workspace = LSApplicationWorkspace.defaultWorkspace()


_timediff = 978307200

class App (object):
    def __init__(self, app):
        try:
            app.applicationIdentifier()
        except AttributeError:
            raise AttributeError('{0} is not an app ObjC Class'.format(app))
        bg = []
        self.app = app
        self.beta = self.app.isBetaApp()
        self.redownload = self.app.isPurchasedReDownload()
        self.name = str(self.app.localizedName())
        self.type = str(self.app.bundleType())
        self.version = str(self.app.bundleVersion())
        self.fileSharing = self.app.fileSharingEnabled()
        self.settingsBundle = self.app.hasSettingsBundle()
        for b in self.app.UIBackgroundModes():
            bg += [str(b)]
        self.backgroundModes = bg
        self.vendor = str(self.app.vendorName())
        self.appID = str(self.app.applicationIdentifier())
        if len(self.app.appTags()):
            for i in app.appTags():
                if i == 'hidden':
                    self.hidden = True
        else:
            self.hidden = False
        self.modTime = datetime.fromtimestamp(self.app.bundleModTime()+_timediff)
        dfam = []
        try:
            for i in self.app.deviceFamily():
                dfam += [i]
            if 1 in dfam:
                self.iPhoneUI = True
            else:
                self.iPhoneUI = False
            if 2 in dfam:
                self.iPadUI = True
            else:
                self.iPadUI = False
        except:
            pass
        self.signerID = str(self.app.signerIdentity())
        self.adHoc = self.app.isAdHocCodeSigned()
        self.sdkVersion = str(self.app.sdkVersion())
        self.infoPlist = None
        self.staticDisk = None
        self.dynamicDisk = None
        self.icon = None
        
    def enumURLSchemes(self):
        schemes = []
        returns = []
        for i in workspace.publicURLSchemes():
            schemes += [str(i)]
        for i in schemes:
            app = workspace.applicationForOpeningResource_(_urlHandle(i+'://'))
            if str(app.applicationIdentifier()) == self.appID:
                returns += [i]
            self.schemes = returns
            
    def getDiskUsage(self):
        """Set's the static and dynamic disk usage variables"""
        # Static might be the app install size
        self.staticDisk = self.app.staticDiskUsage().integerValue()
        # Dynamic might be the storage usage
        self.dynamicDisk = self.app.dynamicDiskUsage().integerValue()
        
    def getInfoPlist(self):
        """Set's the info.plist for an app"""
        self.infoPlist = self.app._infoDictionary().propertyList()
        
    def getIcon(self, scale=2.0, form=10):
        i=UIImage._applicationIconImageForBundleIdentifier_format_scale_(self.appID, form, scale)
        o=ObjCInstance(i.akCGImage())
        t=UIImage.imageWithCGImage_(o)
        d=uiimage_to_png(t)
        buffer = BytesIO(d)
        self.icon = Image.open(buffer)
        
        
    def __str__(self):
        return self.appID

    def __repr__(self):
        return '<'+self.appID+'>'


def _objcDict(objcd):
    returns = []
    for i in zip(objcd.allKeys(), objcd.allValues()):
        returns += [{i[0]: i[1]}]
    return returns


def _urlHandle(url):
    if type(url) != ObjCInstance:
        return nsurl(url)
    if url.isKindOfClass_(ObjCClass('NSURL')):
        return url


def installed(bid):
    if type(bid) != str:
        raise TypeError
    return workspace.applicationIsInstalled_(bid)


def openURL(url):
    return workspace.openURL_(_urlHandle(url))


def canOpenURL(url):
    if workspace.applicationForOpeningResource_(_urlHandle(url)):
        return True
    return False


def URLOpensIn(url):
    opener = workspace.applicationForOpeningResource_(_urlHandle(url))
    if opener:
            return App(opener)
    return None
    

def openWithBundleID(bid):
    if type(bid) == str:
        workspace.openApplicationWithBundleID_(bid)
        return True
    else:
        return False
        

def allApps():
    apps = workspace.allInstalledApplications()
    returns = []
    for i in apps:
        returns += [App(i)]
    return returns


def enumUrlSchemes():
    returns = []
    schemes = []
    for i in workspace.publicURLSchemes():
        schemes += [str(i)]
    for i in schemes:
        app = workspace.applicationForOpeningResource_(_urlHandle(i+'://'))
        returns += [{'scheme': i,'app': App(app)}]
    return returns


def backgroundApps():
    returns = []
    for i in workspace.applicationsWithUIBackgroundModes():
        returns += [App(i)]
    return returns
    
    
def audioComponentApps():
    returns = []
    for i in workspace.applicationsWithAudioComponents():
        returns += [App(i)]
    return returns
    

def overideChecker(url):
    url=_urlHandle(url)
    return workspace.URLOverrideForURL_(url)


def getVendors(applist=allApps()):
    vendors = []
    for i in applist:
        if i.vendor not in vendors:
            vendors += [i.vendor]
    return vendors


def getPythonista():
    returns = []
    for i in allApps():
        if 'Pythonista' in i.appID:
            returns += [i]
    
    return returns
