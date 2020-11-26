from sardana.macroserver.macro import Macro, macro, Type
from tango import DeviceProxy

mte_device_name = 'rsxs/lightfield/mte'

@macro()
def mte_fullchip(self):
    """Macro mte_fullchip"""
    self.output("Running mte_fullchip...")
    mte = DeviceProxy(mte_device_name)
    mte.set_binning(1)


@macro([
    ['roi_name', Type.String, None, 'name of the roi in Environment/LaVue'],
    ['binning', Type.Integer, 1, 'binning of MTE camera'],
    ['image_name', Type.String, 'mte', 'name of image in measurement group'],
])
def mte_roi_set(self, roi_name, binning, image_name):
    """Macro mte_roi_set
    read roi from env and set in lighfield
    additionally update measurement group dimensions of mte 2Dcounter """
    ret = self.execMacro('roi_read', roi_name, 0)
    roi = ret.getResult()
    
    active_meas_grp = self.getEnv('ActiveMntGrp')
    meas_grp = self.getMeasurementGroup(active_meas_grp)
    image = meas_grp.getEnabled(image_name)
    #self.output(image)

    mte = DeviceProxy(mte_device_name)
    mte.set_roi([roi[0], roi[2], roi[1], roi[3], binning])
    self.output('Set MTE ROI to\nx0: {:d} x1: {:d}\ny0: {:d} y1: {:d}\nbinning: {:d}'.format(roi[0], roi[2], roi[1], roi[3], binning))
    self.output('MTE image shape [{:d}, {:d}]'.format(int((roi[3]-roi[1])/binning), int((roi[2]-roi[0])/binning)))
    

@macro()
def mte_temp_get(self):
    """Macro mte_temp_get"""
    mte = DeviceProxy(mte_device_name)
    self.output('Current Temperature: \t {:0.1f} C'.format(mte.temp_read))
    self.output('SetPoint Temperature: \t {:0.1f} C'.format(mte.temp_set))
    if mte.temp_status == 2:
        self.output('Temperature is locked!')
    else:
        self.output('Temperature is unlocked!')


@macro([['set_point', Type.Float, None, 'Set point temperature of camera [C]']])
def mte_temp_set(self, set_point):
    """Macro mte_temp_set"""
    mte = DeviceProxy(mte_device_name)
    mte.temp_set = set_point
    self.output('Temperature set to: \t {:0.1f} C'.format(mte.temp_set))

