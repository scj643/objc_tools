__doc__ = '''This lib is for making ObjCBlocks useful.
             DO NOT USE from objc_tools.blocks import * This module relys on it's name'''
from objc_util import ObjCBlock, c_void_p
from uuid import uuid4
from sys import modules
#global _objects
_objects = {}


class Block (object):
    def __init__(self, argtypes=[c_void_p, c_void_p], restype=None):
        self.block = ObjCBlock(self.handler, argtypes=argtypes, restype=restype)
        
    def handler(_cmd, *args):
        global id
        id = uuid4()
        this = modules[__name__]
        handled = []
        for i in args:
            handled += [i]
        this._objects[id] = handled
        return id
            
    def check_for_objects(self, block_exec=True, ident = None):
        '''Checks for objects in the _objects global and returns them
           param: block_exec: Block until their are objects, if False will just pass with None if nothing is found
        '''
        this = modules[__name__]
        if not ident:
            if this.id:
                ident = this.id
            else:
                raise NameError('No IDs')
                return None
        if block_exec:
            while not any(this._objects[ident]):
                pass
        returns = this._objects[ident]
        del this._objects[ident]
        return returns
            
