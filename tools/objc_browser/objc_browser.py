#def run():
import ui
from objc_util import ObjCClass, ObjCInstance, UIColor
from objc_tools import bundles
import dialogs
import clipboard

class loading (ui.View):
    def __init__(self):
        self.activity = ui.ActivityIndicator(name='activity', hides_when_stopped=True, style = ui.ACTIVITY_INDICATOR_STYLE_WHITE_LARGE, touch_enabled = False)
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
    frameworks['No Framework'] = {'bundle': None, 'items': []}
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
            frameworks['No Framework']['items'] += [i]
    flist = sorted(frameworks.keys())
    return {'flist': flist, 'frameworks': frameworks}
    
class FrameworkClassesDataSource(object):
    '''Pass the items from get_frameworks
    >>> d = get_frameworks()
    >>> h = FrameworkClassesDataSource(d['frameworks']['com.apple.UIKit'])'''
    def __init__(self, fwork_items):
        self.items = fwork_items['items']
        self.name = fwork_items['bundle'].bundleID

    def tableview_did_select(self, tableview, section, row):
        pass

    def tableview_number_of_sections(self, tableview):
        return 1

    def tableview_number_of_rows(self, tableview, section):
        return len(self.items)

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.text_label.text = self.items[row]
        cell.accessory_type = 'detail_disclosure_button'
        return cell

    def tableview_title_for_header(self, tableview, section):
        return self.name

class CopyDelegate (object):
    def tableview_did_select(self, tableview, section, row):
        tableview.selected_row = -1
        clipboard.set(tableview.data_source.items[row])
        dialogs.hud_alert('copied')
    
    def tableview_accessory_button_tapped(self, tableview, section, row, **kwargs):
        v = ui.TableView()
        v.name = tableview.data_source.items[row]
        v.data_source = ClassBrowserController(tableview.data_source.items[row])
        v.autoresizing = 'wh'
        v.reload()
        if ui.get_window_size().width <= 320:
            v.present('full_screen')
        else:
            v.width=600
            v.height=200
            v.present('popover', popover_location=(0,0))

class ClassBrowserController(object):
    def __init__(self, cla=''):
        self.class_name = cla
        self.obs = []
        try:
            c = ObjCClass(self.class_name)
        except ValueError:
            dialogs.alert(self.class_name + ' is not a known class')
        try:
            self.obs.append(['Class',dir(c.alloc())])
        except:
            pass

    def tableview_did_select(self, tableview, section, row):
        clipboard.set(self.obs[section][1][row])
        tableview.close()

    def tableview_number_of_sections(self, tableview):
        return len(self.obs)

    def tableview_number_of_rows(self, tableview, section):
        return len(self.obs[section][1])

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.text_label.text = self.obs[section][1][row]
        return cell

    def tableview_title_for_header(self, tableview, section):
        return self.obs[section][0]
        


class InfoDataSource (object):
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
        v.data_source = InfoDataSource(obj)
        v.autoresizing = 'wh'
        v.reload()
        if ui.get_window_size().width <= 320:
            v.present('full_screen')
        else:
            v.width=300
            v.height=200
            v.present('popover')

        
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
        #print('section: ', section, ' row: ', row)
        cell.text_label.text = self.fworks['flist'][row].split('.')[-1]
        cell.accessory_type = 'detail_disclosure_button'
        return cell

    def tableview_title_for_header(self, tableview, section):
        return 'Framework'

@ui.in_background
def reload_data(sender, response = 'Reloaded'):
    sender.superview['fwcontainer']['activity'].start()
    sender.enabled = False
    frameworks.fworks = get_frameworks()
    sender.superview['fwcontainer']['classes'].reload()
    ui.in_background(dialogs.hud_alert('Reloaded'))
    sender.enabled = True
    sender.superview['fwcontainer']['activity'].stop()

def run():
    global frameworks
    v = ui.load_view('objc_browser')
    v.background_color = 'efeff4'
    a=loading()
    a.name = 'activity'
    v['fwcontainer'].add_subview(a)
    v['fwcontainer']['activity'].center = v['fwcontainer'].center
    v['fwcontainer']['classes'].delegate = FrameworkClassesDelegate()
    v['selected'].delegate = CopyDelegate()
    v.present('panel')
    v['reload'].enabled = False
    frameworks = AllFrameworksDataSource(get_frameworks())
    v['fwcontainer']['classes'].data_source = frameworks
    reload_data(v['reload'], "Loaded")
    
    #v['classes'].reload()
    
    #h = FrameworkClassesDataSource(d['frameworks']['com.apple.UIKit'])
    
    #v['selected'].data_source = h
    #v['selected'].reload()
    
    #run()
    
    
if __name__ == '__main__':
    run()
