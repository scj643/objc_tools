from objc_util import ObjCClass, nsurl, ObjCInstance, uiimage_to_png, UIImage
from datetime import datetime
from io import BytesIO
from PIL import Image
from objc_tools.objc_json import objc_to_py

LSApplicationWorkspace = ObjCClass('LSApplicationWorkspace')
workspace = LSApplicationWorkspace.defaultWorkspace()
LSApplicationProxy = ObjCClass('LSApplicationProxy')

_timediff = 978307200

class App (object):
    def __init__(self, app):
        try:
            app.applicationIdentifier()
        except AttributeError:
            raise AttributeError('{0} is not an app ObjC Class'.format(app))
        bg = []
        self.objc = app
        if len(self.objc.appTags()):
            for i in app.appTags():
                if i == 'hidden':
                    self.hidden = True
        else:
            self.hidden = False
        self.modTime = datetime.fromtimestamp(self.objc.bundleModTime()+_timediff)
        try:
            dfam = [i.intValue() for i in self.objc.deviceFamily()]
        except:
            dfam = []
        self.iPhoneUI = 1 in dfam
        self.iPadUI = 2 in dfam
        self.infoPlist = None
        self.staticDisk = None
        self.dynamicDisk = None
        self.icon = None
        
    @property
    def isBeta(self):
        return self.objc.isBetaApp()
        
    @property
    def isRedownload(self):
        return self.objc.isPurchasedReDownload()
        
    @property
    def name(self):
        return str(alocalizedName())
        
    @property
    def type(self):
        return str(self.objc.bundleType())
        
    @property
    def version(self):
        return str(self.objc.bundleVersion())
        
    @property
    def fileSharing(self):
        return self.objc.fileSharingEnabled()
        
    @property
    def hasSettingsBundle(self):
        return self.objc.hasSettingsBundle()
        
    @property
    def backgroundModes(self):
        return [str(mode) for mode in self.objc.UIBackgroundModes()]


    @property
    def vendor(self):
        return str(self.objc.vendorName())
    
    @property
    def appID(self):
        return str(self.objc.applicationIdentifier())
        
    @property
    def signerID(self):
        return str(self.objc.signerIdentity())
        
    @property
    def adHoc(self):
        return self.objc.isAdHocCodeSigned()
        
    @property
    def sdkVersion(self):
        return str(self.objc.sdkVersion())
        
    @property
    def entitlements(self):
        try:
            return objc_to_py(self.objc.entitlements())
        except TypeError:
            return None
        
    def enumURLSchemes(self):
        returns = []
        for i in [str(i) for i in workspace.publicURLSchemes()]:
            app = workspace.applicationForOpeningResource_(_urlHandle(i+'://'))
            if str(app.applicationIdentifier()) == self.appID:
                returns += [i]
            self.schemes = returns
            
    def getDiskUsage(self):
        """Set's the static and dynamic disk usage variables"""
        # Static might be the app install size
        self.staticDisk = self.objc.staticDiskUsage().integerValue()
        # Dynamic might be the storage usage
        self.dynamicDisk = self.objc.dynamicDiskUsage().integerValue()
        
    def getInfoPlist(self):
        """Set's the info.plist for an app"""
        self.infoPlist = self.objc._infoDictionary().propertyList()
        
    def getIcon(self, scale=2.0, form=10):

        i = UIImage._applicationIconImageForBundleIdentifier_format_scale_(self.appID, form, scale)
        o = ObjCInstance(i.akCGImage())
        img = UIImage.imageWithCGImage_(o)
        with BytesIO(uiimage_to_png(img)) as buffer:
            self.icon = Image.open(buffer)

    def __str__(self):
        return self.appID

    def __repr__(self):
        return '<' + self.appID + '>'


def _objcDict(objcd):
    returns = []
    for i in zip(objcd.allKeys(), objcd.allValues()):
        returns += [{i[0]: i[1]}]
    return returns


def _urlHandle(url):
    if not isinstance(url, ObjCInstance):
        return nsurl(url)
    return url if url.isKindOfClass_(ObjCClass('NSURL')) else None


def installed(bid):
    if not isinstance(bid, str):
        raise TypeError
    return workspace.applicationIsInstalled_(bid)


def openURL(url):
    return workspace.openURL_(_urlHandle(url))


def canOpenURL(url):
    return bool(workspace.applicationForOpeningResource_(_urlHandle(url)))


def URLOpensIn(url):
    opener = workspace.applicationForOpeningResource_(_urlHandle(url))
    return App(opener) if opener else None
  

def openWithBundleID(bid):
    if isinstance(bid, str):
        workspace.openApplicationWithBundleID_(bid)
        return True
    else:
        return False
        

def allApps():
    return [App(app) for app in workspace.allInstalledApplications()]


def enumUrlSchemes():
    returns = []
    for i in [str(i) for i in workspace.publicURLSchemes()]:
        app = workspace.applicationForOpeningResource_(_urlHandle(i+'://'))
        returns += [{'scheme': i,'app': App(app)}]
    return returns


def backgroundApps():
    '''Broken in iOs 10 Needs Rewrite'''
    return [App(app) for app in workspace.applicationsWithUIBackgroundModes()]


def audioComponentApps():
    '''Broken in iOS 10 Needs Rewrite'''
    return [App(app) for app in workspace.applicationsWithAudioComponents()]


def overideChecker(url):
    return workspace.URLOverrideForURL_(_urlHandle(url))


def getVendors(applist=allApps()):
    return sorted(set(app.vendor for app in applist))


def getPythonista():
    return [app for app in allApps() if 'Pythonista' in app.appID]


def getAppByBID(bid):
    a=LSApplicationProxy.applicationProxyForIdentifier_(bid)
    if not a.appState().isValid():
        raise NameError('Not a valid BID')
    else:
        return App(a)

