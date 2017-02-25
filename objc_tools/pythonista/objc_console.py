__doc__ = '''A lib for working with the objc functions of the console view'''
from objc_util import ObjCClass, UIApplication

console = UIApplication.sharedApplication().\
                        keyWindow().rootViewController().\
                        accessoryViewController().\
                        consoleViewController()
