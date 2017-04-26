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
    if not alloc:
        py_methods = []
        functions = []
    functions = [x for x in py_methods if x not in initializers]
    return {
        'Initializers': initializers,
        'Methods': functions,
        'PyMethods': py_methods
    }


class ObjCClassInfo(object):
    def __init__(self, cls, alloc = True):
        if isinstance(cls, (ObjCClass)):
            self.name = cls.class_name.decode('utf-8')
        if isinstance(cls, (ObjCInstance)):
            self.name = cls._get_objc_classname().decode('utf-8')
        if isinstance(cls, (str)):
            self.name = cls
        objects = class_objects(self.name, alloc)
        if alloc:
            self.get_methods()
        else:
            self.nethods = []
        self.initializers = objects['Initializers']
        if bundles.bundleForClass(self.name):
            self.bundleID = bundles.bundleForClass(self.name).bundleID
        else:
            self.bundleID = None
        self.alloc = alloc
    
    def get_methods(self):
        self.methods = class_objects(self.name)['Methods']

    def superclass(self, alloc = False):
        if 'superclass' in self.initializers:
            if ObjCClass(self.name).superclass():
                return ObjCClassInfo(
                    ObjCInstance(ObjCClass(self.name).superclass()), alloc)
            else:
                return None
        else:
            return None

    @property
    def class_depth(self):
        steps = 0
        parent = self.superclass()
        while parent:
            parent = parent.superclass()
            steps += 1
        return steps - 1

    def get_class_at_depth(self, value):
        if value > self.class_depth:
            raise ValueError('Class_depth too big')
        current_depth = 0
        current_class = self.superclass
        while current_depth != class_depth:
            current_class = current_class.superclass
            current_depth += 1

    def inhereted_methods(self):
        items = []
        parent = self.superclass()
        while parent:
            items += [i for i in parent.methods if i not in items]
            parent = parent.superclass()
        return items
        
    def inhereted_initalizers(self):
        items = []
        parent = self.superclass(False)
        while parent:
            items += [i for i in parent.initializers if i not in items]
            parent = parent.superclass(False)
        return items

    def objc_class(self):
        return ObjCClass(self.name)

    def shared_init(self):
        shared = [i for i in self.initializers if re.search('shared', i, re.I)]
        if shared:
            return shared
        else:
            return None

    def default_init(self):
        default = [
            i for i in self.initializers if re.search('default', i, re.I)
        ]
        if default:
            return default
        else:
            return None

    def __repr__(self):
        return '<ObjCClassInfo: {} <sharedInit: {}, defaultInit: {}>'.format(
            self.name, bool(self.shared_init()), bool(self.default_init()))


def get_classes_for_bundle(bundle, regex=True, class_imfo=True, alloc = False):
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
                    if bundle in bundles.bundleForClass(i).bundleID:
                        results += [i]
    if class_imfo:
        results = [ObjCClassInfo(i) for i in results]
    return results


def stat_dict(info_list, ignore_inheretence=False):
    # ignoring inheretence is very time consuming
    all_init = {}
    for i in info_list:
        for g in i.initializers:
                if ignore_inheretence and g in i.inhereted_initalizers():
                    pass
                else:
                    if g in all_init.keys():
                        all_init[g] += [i]
                    else:
                        all_init[g] = [i]
    return all_init
    
    
if __name__ == '__main__':
    from pprint import pprint as p
    from objc_util import load_framework
    from timeit import timeit
    load_framework('SceneKit')
    #s = get_classes_for_bundle('.*UIKit.*')
    #print('got classes')
    #d = stat_dict(s, True)
