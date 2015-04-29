import unittest
import deviceAPIUtils
import clr
clr.AddReferenceToFileAndPath("DeviceDLL/DeviceDLL/bin/Debug/DeviceDLL.dll")
import api as devapi

class deviceAPIUtilsTest(unittest.TestCase):
    
    def testCanBrightenNotCLR(self):
        self.assertFalse(deviceAPIUtils.canBrighten(10))
        self.assertFalse(deviceAPIUtils.canBrighten('a string'))
        somePythonTypeObject = ['this is', 'a list of python strings', 'not a .NET class']
        self.assertFalse(deviceAPIUtils.canBrighten(somePythonTypeObject))
        
    def testCanBrightenIsEnableable(self):
        someIEnableable = devapi.CeilingFan(None, None)
        self.assertFalse(deviceAPIUtils.canBrighten(someIEnableable))
        
    def testCanBrightenWrongIReadable(self):
        wrongGenericIReadable = devapi.Thermostat(None, None)
        self.assertFalse(deviceAPIUtils.canBrighten(wrongGenericIReadable))
    
    def testCanBrightenIsLight(self):
        lightswitch = devapi.LightSwitch(None, None)
        lightswitch.Enabled = True
        self.assertTrue(deviceAPIUtils.canBrighten(lightswitch))
        
if __name__ == '__main__':
    unittest.main()