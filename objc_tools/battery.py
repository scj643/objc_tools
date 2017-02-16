from objc_util import ObjCClass, NSBundle

#__all__ = ['battery','backlight_level','set_backlight_level']
UIDevice = ObjCClass('UIDevice')
device = UIDevice.currentDevice()
battery_states = {1: 'unplugged', 2: 'charging', 3: 'full'}

class battery(object):

    def __init__(self):
        device.setBatteryMonitoringEnabled(True)
        
    def __enter__(self):
        device.setBatteryMonitoringEnabled(True)
        return self
    
    def charge_status(self):
        return battery_states[device.batteryState()]
    
    def level(self):
        return device.batteryLevel()

    def __exit__(self, exc_type, exc_value, traceback):
        device.setBatteryMonitoringEnabled(False)

def backlight_level():
    return device._backlightLevel()

def set_backlight_level(value):
    if type(value) == float:
        if 0<= value <= 1:
            device._setBacklightLevel_(value)
