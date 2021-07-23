from objc_util import c_void_p, c_char_p, c_int, c_int32, c, c_long, c_ulong
from objc_tools.c.objc_handler import chandle

dispatch_queue_create = c.dispatch_queue_create
dispatch_queue_create.argtypes = [c_char_p, c_int]
dispatch_queue_create.restype = c_void_p
dispatch_queue_create.errhandle = chandle

dispatch_get_global_queue = c.dispatch_get_global_queue
dispatch_get_global_queue.argtypes = [c_long, c_ulong]
dispatch_get_global_queue.restype = c_void_p
dispatch_get_global_queue.errhandle = chandle

q=dispatch_queue_create(c_char_p(b'com.scj643'), 0)

dispatch_queue_attr_make_with_qos_class = c.dispatch_queue_attr_make_with_qos_class
