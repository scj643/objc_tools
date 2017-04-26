__doc__ = '''A lib for working with the objc functions of the console view'''
from objc_util import ObjCClass, UIApplication, ns
from objc_tools.objc_json import objc_to_py

console = UIApplication.sharedApplication().\
                        keyWindow().rootViewController().\
                        accessoryViewController().\
                        consoleViewController()
                        

class history (object):
    def __init__(self, objc):
        self._objc = console.history
        self._objc_set = console.setHistory_
        self._current_item = console.historyCurrentItem
        
    @property
    def items (self):
        return objc_to_py(self._objc())
        
    @items.setter
    def items (self, items):
        self._objc_set(ns(items))
        
    @property
    def current_item(self):
        return objc_to_py(self._current_item())
        
class Console (object):
    def __init__(self, objc = UIApplication.sharedApplication().\
                        keyWindow().rootViewController().\
                        accessoryViewController().\
                        consoleViewController()):
        self.objc = objc
