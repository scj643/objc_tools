
import ui
from objc_util import (ObjCClass, ObjCInstance, UIColor, byref, c_uint,
                       class_copyMethodList, free, method_getName, sel_getName)
from objc_tools import bundles
import dialogs
import clipboard
import re
from sys import argv
import json
import os
                

def config_handler():
    global objc_browser_conf
    conf_path = os.path.expanduser('~/Documents/objc_browser_conf/')
    conf_filename = 'conf.json'
    objc_browser_conf = {}
    default_conf = {'FrameworkClassesHighlight': [('.*shared', '#bff7ff'), ('.*default', '#95ff9e')],
                    'ClassBrowserHighlight': [('.*shared', '#bff7ff'), ('.*default', '#95ff9e'),
                                              ('set', '#caeaff'), ('.*Error', '#f5ba7a'),
                                              ('.*delegate', '#b780ff')],
                    'AllFrameworksHighlight': [('/System/Library/Frameworks/', '#edffdf'),
                                               ('/System/Library/PrivateFrameworks/', '#ffd5d5'),
                                               ('.*Pythonista3', '#95ff9e')]}
    if not os.path.exists(conf_path):
        os.mkdir(conf_path)
    if os.path.exists(conf_path + conf_filename):
        with open(conf_path + conf_filename, 'r') as f:
            objc_browser_conf = json.load(f)
    else:
        with open(conf_path + conf_filename, 'w') as f:
            json.dump(default_conf, f, indent=4)
    unmatched = set(default_conf) - set(objc_browser_conf)
    if unmatched:
        for key in unmatched:
            objc_browser_conf[key] = default_conf[key]
        with open(conf_path + conf_filename, 'w') as f:
            json.dump(objc_browser_conf, f, indent=4)


def matchcell(item, match_lists):
    for i in match_lists:
        res = None
        p = re.compile(i[0])
        if isinstance(item, list):
            res = any([p.match(x) for x in item])
        if isinstance(item, str):
            res = p.match(item)
        if res:
            return i[1]
    return 'white'

        
class SearchMethods (object):
    def __init__(self, present_mode = 'popover'):
        self.sender = None
        self.present_mode = present_mode
        
    def filter_shared(self, items):
        results = []
        for i in items:
            current = None
            modified = i
            res = [item for item in i['items'] if (matchcell(class_objects(item, False)[0][1], [['.*share', 'yes']]) != 'white')]
            if res:
                current = i
                current['items'] = res
                results += [current]
            
        return results
    
    def started_handler(self, sender):
        # Needed incase the view is dismissed
        self.view = ui.load_view('search')
        self.view['Filter'].clear_button_mode = 'always'
        self.view['Filter'].action = self.do_search
        self.view['results'].delegate = self.CopyDelegate()
        self.sender = sender
        if sender:
            popover_location = sender.center.as_tuple()
        else:
            popover_location = (0,0)
        self.view.present(self.present_mode, popover_location = popover_location)
        
    def do_search(self, sender):
        if self.view['shared_only'].value:
            res = self.filter_shared(self.search(self.view['Filter'].text))
        else:
            res = self.search(self.view['Filter'].text)
        self.view['results'].data_source = FrameworkSearchDataSource(res)
        self.view['results'].reload()
        
    def search(self, query):
        q = re.compile(query)
        results = []
        for k, v in frameworks.fworks['frameworks'].items():
            bresult = {'bundle': v['bundle'], 'items': []}
            bresult['items'] = [item for item in v['items'] if q.match(item)]
            if bresult['items']:
                results += [bresult]
        return results
        
    class CopyDelegate (object):
        def tableview_did_select(self, tableview, section, row):
            tableview.selected_row = -1
            clipboard.set(tableview.data_source.items[section]['items'][row])
            dialogs.hud_alert('copied')
    
        def tableview_accessory_button_tapped(self, tableview, section, row, **kwargs):
            t = ui.TableView()
            v = ui.NavigationView(t)
            v.name = tableview.data_source.items[section]['items'][row]
            t.data_source = ClassBrowserController(v.name)
            t.delegate = SuperClassDelegate()
            v.autoresizing = 'wh'
            t.reload()
            if ui.get_window_size().width <= 320:
                v.present('full_screen')
            else:
                v.width = 600
                v.height = 800
                v.flex = 'HR'
                v.present('popover', popover_location=(0, 0))
        
    
class FrameworkSearchDataSource (object):
    '''Pass the items from frameworks_search
    >>> d = SearchMethods.search('*.AV')
    '''
    def __init__(self, result):
        self.items = result

    def tableview_did_select(self, tableview, section, row):
        pass

    def tableview_number_of_sections(self, tableview):
        return len(self.items)

    def tableview_number_of_rows(self, tableview, section):
        return len(self.items[section]['items'])

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.text_label.text = self.items[section]['items'][row]
        l = class_objects(self.items[section]['items'][row], False)[0][1]
        cell.background_color = matchcell(l, objc_browser_conf['FrameworkClassesHighlight'])
        cell.accessory_type = 'detail_disclosure_button'
        return cell

    def tableview_title_for_header(self, tableview, section):
        if self.items[section]['bundle']:
            return self.items[section]['bundle'].bundleID
        else:
            return 'None'


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
        return [['Initializers', initializers], ['Methods', functions]]


class loading (ui.View):
    def __init__(self):
        self.activity = ui.ActivityIndicator(name='activity', hides_when_stopped=True, style=ui.ACTIVITY_INDICATOR_STYLE_WHITE_LARGE, touch_enabled=False)
        self.activity.center = self.center
        self.add_subview(self.activity)
        self.touch_enabled = False
        self._objc = ObjCInstance(self.activity)
        self._objc.setColor_(UIColor.grayColor())

    def laytout(self):
        self.activity.center = self.superview.center

    def start(self):
        self.bring_to_front()
        self.activity.start()

    def stop(self):
        self.send_to_back()
        self.activity.stop()


def get_classes():
    classes = {}
    classes['No Class'] = []
    for i in ObjCClass.get_names():
        if bundles.bundleForClass(i):
            try:
                if classes[bundles.bundleForClass(i).bundleID]:
                    classes[bundles.bundleForClass(i).bundleID] += [i]
                else:
                    classes[bundles.bundleForClass(i).bundleID] = [i]
            except KeyError:
                classes[bundles.bundleForClass(i).bundleID] = [i]
        else:
            classes['No Class'] += [i]
    clist = []
    for k, v in classes.items():
        clist += [[k, v]]
    return clist


def get_frameworks():
    flist = []
    frameworks = {}
    # Currently not working
    # frameworks['No Framework'] = {'bundle': None, 'items': []}
    for i in ObjCClass.get_names():
        if bundles.bundleForClass(i):
            try:
                if frameworks[bundles.bundleForClass(i).bundleID]:
                    frameworks[bundles.bundleForClass(i).bundleID]['items'] += [i]
                else:
                    frameworks[bundles.bundleForClass(i).bundleID] = {'bundle': bundles.bundleForClass(i), 'items': [i]}
            except KeyError:
                frameworks[bundles.bundleForClass(i).bundleID] = {'bundle': bundles.bundleForClass(i), 'items': [i]}
        else:
            pass

    flist = sorted(frameworks.keys())
    return {'flist': flist, 'frameworks': frameworks}


class FrameworkClassesDataSource(object):
    '''Pass the items from get_frameworks
    >>> d = get_frameworks()
    >>> h = FrameworkClassesDataSource(d['frameworks']['com.apple.UIKit'])'''
    def __init__(self, fwork_items):
        self.items = fwork_items['items']
        if fwork_items['bundle']:
            self.name = fwork_items['bundle'].bundleID
        else:
            self.name = 'None'

    def tableview_did_select(self, tableview, section, row):
        pass

    def tableview_number_of_sections(self, tableview):
        return 1

    def tableview_number_of_rows(self, tableview, section):
        return len(self.items)

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.text_label.text = self.items[row]
        l = class_objects(self.items[row], False)[0][1]
        cell.background_color = matchcell(l, objc_browser_conf['FrameworkClassesHighlight'])
        cell.accessory_type = 'detail_disclosure_button'
        return cell

    def tableview_title_for_header(self, tableview, section):
        return self.items[section]


class FrameworkClassesDelegate (object):
    def tableview_did_select(self, tableview, section, row):
        obj = tableview.data_source.fworks['frameworks'][tableview.data_source.fworks['flist'][row]]
        tableview.superview.superview['selected'].data_source = FrameworkClassesDataSource(obj)
        tableview.superview.superview['selected'].reload()

    def tableview_accessory_button_tapped(self, tableview, section, row, **kwargs):
        obj = tableview.data_source.fworks['frameworks'][tableview.data_source.fworks['flist'][row]]
        v = ui.TableView()
        v.row_height = 120
        v.name = '{} Info'.format(tableview.data_source.fworks['flist'][row].split('.')[-1])
        v.data_source = BundleInfoDataSource(obj)
        v.autoresizing = 'wh'
        v.reload()
        if ui.get_window_size().width <= 320:
            v.present('full_screen')
        else:
            v.width = 300
            v.height = 200
            v.present('popover')


class CopyDelegate (object):
    def tableview_did_select(self, tableview, section, row):
        tableview.selected_row = -1
        clipboard.set(tableview.data_source.items[row])
        dialogs.hud_alert('copied')

    def tableview_accessory_button_tapped(self, tableview, section, row, **kwargs):
        t = ui.TableView()
        v = ui.NavigationView(t)
        v.name = tableview.data_source.items[row]
        t.data_source = ClassBrowserController(tableview.data_source.items[row])
        t.delegate = SuperClassDelegate()
        v.autoresizing = 'wh'
        t.reload()
        if ui.get_window_size().width <= 320:
            v.present('full_screen')
        else:
            v.width = 600
            v.height = 800
            v.flex = 'HR'
            v.present('popover', popover_location=(0, 0))


class SuperClassDelegate (object):
    def tableview_accessory_button_tapped(self, tableview, section, row, **kwargs):
        t = ui.TableView()
        t.data_source = ClassBrowserController(tableview.data_source.obs[0][1][0])
        t.name = tableview.data_source.obs[0][1][0]
        t.delegate = SuperClassDelegate()
        t.reload()
        tableview.navigation_view.push_view(t)


class ClassBrowserController(object):
    def __init__(self, cla=''):
        self.obs = class_objects(cla)
        try:
            self.supercls = ObjCInstance(ObjCClass(cla).superclass())
        except AttributeError:
            self.supercls = None
        self.obs = [['Superclass', [str(self.supercls)]]] + self.obs
        pass

    def tableview_did_select(self, tableview, section, row):
        clipboard.set(self.obs[section][1][row])
        dialogs.hud_alert('copied')

    def tableview_number_of_sections(self, tableview):
        return len(self.obs)

    def tableview_number_of_rows(self, tableview, section):
        return len(self.obs[section][1])

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        if section == 0 and self.obs[section][1][row] not in ['NSObject', 'None']:
            cell.accessory_type = 'detail_disclosure_button'
        cell.text_label.text = self.obs[section][1][row]
        cell.background_color = matchcell(cell.text_label.text, objc_browser_conf['ClassBrowserHighlight'])
        return cell

    def tableview_title_for_header(self, tableview, section):
        return self.obs[section][0]


class BundleInfoDataSource (object):
    def __init__(self, obj):
        self.binfo = obj['bundle']
        self.items = ['Path: {}'.format(self.binfo.path), 'Type: {}'.format(self.binfo.extensionType)]

    def tableview_number_of_rows(self, tableview, section):
        # Return the number of rows in the section
        return len(self.items)

    def tableview_title_for_header(self, tableview, section):
        return "Framework Info"

    def tableview_number_of_sections(self, tableview):
        # Return the number of sections (defaults to 1)
        return 1

    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        cell = ui.TableViewCell()
        cell.text_label.text = self.items[row]
        cell.text_label.number_of_lines = 0
        cell.text_label.line_break_mode = ui.LB_WORD_WRAP
        return cell


class AllFrameworksDataSource(object):
    def __init__(self, fworks):
        self.fworks = fworks

    def tableview_did_select(self, tableview, section, row):
        pass

    def tableview_number_of_sections(self, tableview):
        return 1

    def tableview_number_of_rows(self, tableview, section):
        return len(self.fworks['flist'])

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        # print('section: ', section, ' row: ', row)
        name = self.fworks['flist'][row]
        cell.text_label.text = name.split('.')[-1]
        cell.accessory_type = 'detail_disclosure_button'
        if name in self.fworks['frameworks'].keys():
            if self.fworks['frameworks'][name]['bundle']:
                b = self.fworks['frameworks'][name]['bundle'].path
                cell.background_color = matchcell(b, objc_browser_conf['AllFrameworksHighlight'])
        return cell

    def tableview_title_for_header(self, tableview, section):
        return 'Framework'


@ui.in_background
def reload_data(sender, response='Reloaded'):
    sender.superview['fwcontainer']['activity'].start()
    sender.enabled = False
    frameworks.fworks = get_frameworks()
    sender.superview['fwcontainer']['bundles'].reload()
    sender.superview['fwcontainer']['activity'].stop()
    dialogs.hud_alert('Reloaded')
    sender.enabled = True


def run(search_only=False):
    config_handler()
    global frameworks
    if 'debug' in argv:
        global v
    if 'noui' in argv:
        frameworks = AllFrameworksDataSource(get_frameworks())
        return
    if search_only:
        frameworks = AllFrameworksDataSource(get_frameworks())
        search = SearchMethods('panel')
        search.started_handler(None)
        search.view.autoresizing = 'wh'
        return
    
    v = ui.load_view('objc_browser')
    v.background_color = 'efeff4'
    a = loading()
    a.name = 'activity'
    v['fwcontainer'].add_subview(a)
    v['fwcontainer']['activity'].center = v['fwcontainer'].center
    v['fwcontainer']['bundles'].delegate = FrameworkClassesDelegate()
    v['selected'].delegate = CopyDelegate()
    v.present('panel')
    v['reload'].enabled = False
    frameworks = AllFrameworksDataSource(get_frameworks())
    v['fwcontainer']['bundles'].data_source = frameworks
    reload_data(v['reload'], "Loaded")
    search = SearchMethods()
    v['search'].action = search.started_handler

    # v['classes'].reload()

    # h = FrameworkClassesDataSource(d['frameworks']['com.apple.UIKit'])

    # v['selected'].data_source = h
    # v['selected'].reload()

    # run()


if __name__ == '__main__':
    run()
