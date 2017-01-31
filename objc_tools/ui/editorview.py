from objc_util import UIApplication, ObjCInstance, on_main_thread, ObjCClass, create_objc_class
UIViewController = ObjCClass('UIViewController')


rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
tabVC = rootVC.detailViewController()

@on_main_thread
class EditorTabView (object):
    '''Presents a view as an editor tab
    view: a ui.view
    title: the tab title
    '''
    def __init__(self, view, title = 'test'):
        self.CustomViewController = create_objc_class('CustomViewController', UIViewController)
        self.vc = self.CustomViewController.new().autorelease()
        self.vc.title = title
        self.vc.view = ObjCInstance(view)
        tabVC.addTabWithViewController_(self.vc)
