from objc_util import ObjCClass

UIDevice = ObjCClass('UIDevice')
device = UIDevice.currentDevice()
battery_states = {1: 'unplugged', 2: 'charging', 3: 'full'}

class battery(object):
    __init__(self):
        device.setBatteryMonitoringEnabled(True)
    
    def charging(self):
        
