from objc_util import ObjCInstance, nsurl, NSURL, NSString

def objcDict(objcd):
    returns = []
    for i in zip(objcd.allKeys(), objcd.allValues()):
        returns += [{i[0], i[1]}]
    return returns


    
def urlHandle(url):
    if type(url) != ObjCInstance:
        if type(url) != str:
            raise TypeError('{} is not a string'.format(str(url)))
        url = nsurl(url)
    try:
        url.isKindOfClass_(NSURL)
    except AttributeError:
        raise TypeError('{} is not an NSURL'.format(str(url)))
    if url.isKindOfClass_(NSURL):
        return url
    else:
        raise TypeError('{} is not an NSURL'.format(str(url)))


def type_convert(item):
    try:
        item._cfTypeID()
    except AttributeError:
        raise TypeError('{} is not an ObjC type'.format(str(item)))
    if item.isKindOfClass(NSString):
        return str(item)

    


