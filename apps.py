from objc_util import ObjCClass, nsurl, ObjCInstance

LSApplicationWorkspace = ObjCClass('LSApplicationWorkspace')
workspace = LSApplicationWorkspace.defaultWorkspace()


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
        self.ID = str(self.app.applicationIdentifier())

    def __str__(self):
        return self.ID

    def __repr__(self):
        return self.ID


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
    

def allApps():
    apps = workspace.allInstalledApplications()
    returns = []
    for i in apps:
        returns += [App(i)]
    return returns


def enumOpensIn():
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
