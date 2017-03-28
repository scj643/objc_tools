import re
from objc_tools.backports import stringcase
import clipboard
import editor


ENUM_RE = re.compile(r'typedef (?:NS_ENUM|NS_OPTIONS)+\(.*?\).*?{.*?}', re.S)


def read_header(filename):
    '''read_header Reads a header file and returns a string'''
    with open(filename, 'rb') as f:
        return f.read().decode('utf-8')


class HeaderItem (object):
    '''HeaderItem An item that is a single line from a header enum
    Must be a single line item
    example HeaderItem("UIViewAnimationCurveEaseInOut,         // slow at beginning and end")
    '''
    def __init__(self, text, super_name = '', index_number = None, case_type=str):
        '''
        :case_type: A function for processing a string is passed here
        '''
        self.text = text
        self.index_number = index_number
        self.super_name = super_name
        if 'Options' in self.super_name:
            self.super_name = self.super_name.replace('Options', 'Option')
        self.case_type = case_type
        if self.cmnt:
            self.define = self.text.replace(self.cmnt, '').replace(' ', '').strip('//').rstrip(',').replace(self.super_name, '')
        else:
            self.define = self.text.strip().rstrip(',').replace(self.super_name, '')
        self.name = self.get_name()

    @property
    def cmnt(self):
        q = re.compile('//.*')
        m = q.findall(self.text)
        if m:
            return m[0].strip('//').strip()
        else:
            return None
        
    @property
    def value(self):
        match = re.search('(\d+)\s*<<\s*(\d+|\w+)', self.define)
        if match:
            return match.group(0).replace(' ', '').replace('<<', ' << ')
            
        items = self.define.split(maxsplit=2)
        if '=' in items:
            return items[-1].replace(' ', '')
        else:
            return str(self.index_number)
    
    def get_name(self):
        n = self.define.split()[0]
        match = re.search('=?(\d+)\s*<<\s*(\d+|\w+)', n)
        if match:
            n = n.replace(match.group(0), '')
        t = self.case_type(n)
        if t == 'None':
            t = 'none'
        else:
            return t.strip(',')
    
    def python_string(self, form = stringcase.camelcase):
        if not self.cmnt:
            returns = '{} = {}'.format(form(self.name), self.value)
        else:
            returns = '{} = {} # {}'.format(form(self.name), self.value, self.cmnt)
        return returns
    def __repr__(self):
        return '<HeaderItem {}, super: {}, value: {}>'.format(self.name, self.super_name, self.value)
        


class Header (object):
    '''Header object
    Pass a result that cntains a header enum
    I.E. 
    typedef NS_ENUM(NSInteger, UIViewAnimationCurve) {
        UIViewAnimationCurveEaseInOut,         // slow at beginning and end
        UIViewAnimationCurveEaseIn,            // slow at beginning
        UIViewAnimationCurveEaseOut,           // slow at end
        UIViewAnimationCurveLinear,
    };
    '''
    def __init__(self, text):
        self.text = text
        self.preprocess()
        self.test = self.extract_name_and_type()
        self.name = self.extract_name_and_type()['name']
        self.avaliblity = self.get_avaliblity()
    
    @property
    def type(self):
        if 'NS_ENUM' in self.text:
            return 'IntEnum'
        if 'NS_OPTIONS' in self.text:
            return 'Flag'

    def extract_name_and_type(self):
        r = re.compile(r'.*\(.*,.*\)')
        m = r.findall(self.text)
        if len(m) == 1:
            t = m[0]
            t = t.strip('typedef').strip(')').lstrip().strip('NS_ENUM').strip('NS_OPTIONS').strip('(')
            split = t.split(',')
            items = [item.strip() for item in split]
            if len(items) == 1:
                return {'type': None, 'name': items[0]}
            else:
                return {'type': items[0], 'name': items[-1]}

    def extract_items(self, case_type = str):
        m = re.findall(r'{.*}', self.text, re.S)
        dont_include = re.compile('(^\s*$)|^#|{|}')
        if m:
            items = [item.strip() for item in m[0].splitlines() if (not any(x in item for x in ['{', '}']) and item.strip() and not any(item.startswith(x) for x in ['#', r'//']))]
            returns = [HeaderItem(items[i], self.name, i, case_type) for i in range(0, len(items)-1)]
            return returns
        else:
            return None
            
    def get_avaliblity(self):
        res = re.findall(r'IOS_AVAILABLE\(.*?\)', self.text)
        paren = re.compile('\(.*?\)')
        version = [paren.match(item).group() for item in res]
        
    def preprocess(self):
        api_re = re.compile('API_AVAILABLE\(.*\)')
        m = api_re.findall(self.text)
        for i in m:
            self.text = self.text.replace(i, '')
        
    def convert_to_python(self):
        text = 'class {} ({}):\n'.format(self.name, self.type)
        for i in self.extract_items():
            text += '    {}\n'.format(i.python_string())
        return text
        
        
if __name__ == '__main__':
    text = editor.get_text()
    s = editor.get_selection()
    t = text[s[0]: s[1]]
    #t = read_header('enum.txt')
#    t = 'typedef NS_ENUM(NSInteger, SCNGeometryPrimitiveType) {\n\tSCNGeometryPrimitiveTypeTriangles                                                   = 0,\n\tSCNGeometryPrimitiveTypeTriangleStrip                                               = 1,\n\tSCNGeometryPrimitiveTypeLine                                                        = 2,\n\tSCNGeometryPrimitiveTypePoint                                                       = 3,\n#if defined(SWIFT_SDK_OVERLAY2_SCENEKIT_EPOCH) && SWIFT_SDK_OVERLAY2_SCENEKIT_EPOCH >= 2\n    SCNGeometryPrimitiveTypePolygon API_AVAILABLE(macosx(10.12), ios(10.0), tvos(10.0)) = 4\n#endif\n}'
    string = ''
    for i in ENUM_RE.findall(t):
        string += '{}\n\n'.format(Header(i).convert_to_python())   
    if string:
        clipboard.set(string)
        
    
    # e.extract_items()
    # g = HeaderItem(e.extract_items()[0], e.name)
    #w = HeaderItem('UIViewAnimationOptionAllowUserInteraction      = 1 <<  1, // turn on user interaction while animating', 'UIViewAnimationOptions')
    
    #s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', 'test_test')
    
