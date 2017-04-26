from objc_util import (ObjCClass, ObjCInstance, UIColor, byref, c_uint,
                       class_copyMethodList, free, method_getName, sel_getName)
from objc_tools import bundles
import re


class FrameworkClass(object):
    def __init__(self, name, fetch_classes=False):
        self.name = name
        if fetch_classes:
            pass

    def __repr__(self):
        return '<Framework: <name: {}>>'.format(self.name)


#c = ObjCClass.get_names()
#u=[i for i in c if bundles.bundleForClass(i) and 'UIKit' in bundles.bundleForClass(i).bundleID]
def class_objects(cla='', alloc=True):
    functions = []
    initializers = []
    py_methods = []
    try:
        c = ObjCClass(cla)
    except ValueError:
        dialogs.alert(cla + ' is not a known class')
    try:
        initializers = dir(c)
    except:
        return None
    if alloc:
        num_methods = c_uint(0)
        method_list_ptr = class_copyMethodList(c.ptr, byref(num_methods))
        for i in range(num_methods.value):
            selector = method_getName(method_list_ptr[i])
            sel_name = sel_getName(selector)
            if not isinstance(sel_name, str):
                sel_name = sel_name.decode('ascii')
            py_method_name = sel_name.replace(':', "_")
            if '.' not in py_method_name:
                py_methods.append(py_method_name)
        free(method_list_ptr)
    functions = [x for x in py_methods if x not in initializers]
    return {
        'Initializers': initializers,
        'Methods': functions,
        'PyMethods': py_methods
    }


class ObjCClassInfo(object):
    def __init__(self, cls):
        if isinstance(cls, (ObjCClass)):
            self.name = cls.class_name.decode('utf-8')
        if isinstance(cls, (ObjCInstance)):
            self.name = cls._get_objc_classname().decode('utf-8')
        if isinstance(cls, (str)):
            self.name = cls
        objects = class_objects(self.name)

        self.methods = objects['Methods']
        self.initializers = objects['Initializers']
        if bundles.bundleForClass(self.name):
            self.bundleID = bundles.bundleForClass(self.name).bundleID
        else:
            self.bundleID = None
        if [i for i in self.initializers if re.search('default', i, re.I)]:
            self.default_init = True
        else:
            self.default_init = False
        if [i for i in self.initializers if re.search('shared', i, re.I)]:
            self.shared_init = True
        else:
            self.shared_init = False

    def __repr__(self):
        return '<ObjCClassInfo: {} <sharedInit: {}, defaultInit: {}>'.format(
            self.name, self.shared_init, self.default_init)


def get_classes_for_bundle(bundle, regex=True, class_imfo=True):
    results = []
    if isinstance(bundle, (str)) and regex:
        search = re.compile(bundle)
    if isinstance(bundle, (type(re.compile('')))):
        search = bundle
    for i in ObjCClass.get_names():
        if bundles.bundleForClass(i):
            if regex:
                if isinstance(bundles.bundleForClass(i).bundleID, (str)):
                    if search.match(bundles.bundleForClass(i).bundleID):
                        results += [i]
            else:
                if isinstance(bundles.bundleForClass(i).bundleID, (str)):
                    if bundles.bundleForClass(i).bundleID.find(bundle) != -1:
                        results += [i]
    if class_imfo:
        results = [ObjCClassInfo(i) for i in results]
    return results


if __name__ == '__main__':
    s = get_classes_for_bundle('.*UIKit.*')

