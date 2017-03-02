#**************************************************************
#*                                                            *
#*   Copyright (C) Microsoft Corporation. All rights reserved.*
#*                                                            *
#**************************************************************

import dbus
import dbus.service
import collections
import obmc_dbuslib
import math
import obmc.gpio_lib

from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
from utils import completion_code

bus = get_dbus()

gpiolib = obmc.gpio_lib.GpioLib()

gpiolib.InitGpio('PSU1_PRSNT_N')
gpiolib.InitGpio('PSU2_PRSNT_N')

DBUS_NAME = 'org.openbmc.Sensors'
DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'

SENSOR_VALUE_INTERFACE = 'org.openbmc.SensorValue'
SENSOR_THRESHOLD_INTERFACE = 'org.openbmc.SensorThresholds'
SENSOR_HWMON_INTERFACE = 'org.openbmc.HwmonSensor'

MAX_PSU_NUM = 2

def get_sensor_name(sensor_path):
    path_list = sensor_path.split("/")
    return path_list[-1]

sensor_power_control_table =\
[\
    "/org/openbmc/sensors/Fans/Fan_HSC_Power_Out",\
    "/org/openbmc/sensors/Fans/Fan_HSC_Status",\
    "/org/openbmc/sensors/Fans/Fan_HSC_Status_MFR"\
]

sensor_power_voltage_table =\
[\
    "/org/openbmc/sensors/Fans/Fan_HSC_Volt_Out",\
    "/org/openbmc/sensors/PowerSupply1/PSU1_Volt_Out",\
    "/org/openbmc/sensors/PowerSupply2/PSU2_Volt_Out",\
    "/org/openbmc/sensors/Power/Voltages/P12V",\
    "/org/openbmc/sensors/Power/Voltages/P3V3_A",\
    "/org/openbmc/sensors/Power/Voltages/P1V15_AUX",\
    "/org/openbmc/sensors/Power/Voltages/P1V2_AUX",\
    "/org/openbmc/sensors/Power/Voltages/P5V_AUX",\
    "/org/openbmc/sensors/Power/Voltages/P12V_AUX",\
    "/org/openbmc/sensors/Power/Voltages/P3V3_AUX",\
    "/org/openbmc/sensors/Power/Voltages/P3V_BAT"\
]

sensor_power_powersupplies_table =\
[\
    "/org/openbmc/sensors/PowerSupply1/PSU1_Power_Out",\
    "/org/openbmc/sensors/PowerSupply2/PSU2_Power_Out"
]

def GetPsuPresent(psu_num):
    gpio_path = gpiolib.sys_gpio_path['PSU'+str(psu_num)+'_PRSNT_N']

    with open (gpio_path, 'r') as f:
        for line in f:
            present = line.rstrip('\n')

    if present == '0':
        return 1
    else:
        return 0

def get_chassis_power():
    result = {}
    result['Voltages'] = collections.OrderedDict()

    try:
        # PowerControl
        result['fan_HSC_Power_sensor_name'] = get_sensor_name(sensor_power_control_table[0])
        result['power_consumed_watts'] = ''
        result['HSC_status'] = '0x00'
        result['HSC_status_MFR'] = '0x00'

        object = bus.get_object(DBUS_NAME, sensor_power_control_table[0]) #Fan_HSC_Power_Out
        interface = dbus.Interface(object, DBUS_INTERFACE)

        adjust = interface.Get(SENSOR_HWMON_INTERFACE, 'adjust')
        scale = interface.Get(SENSOR_HWMON_INTERFACE, 'scale')
        value = interface.Get(SENSOR_VALUE_INTERFACE, 'value')
        
        result['power_consumed_watts'] = value * math.pow(10, scale) * adjust

        #Voltages
        for index in range(0, len(sensor_power_voltage_table)-1):
            property = {}
            property['sensor_id'] = index+1
            property['sensor_name'] = get_sensor_name(sensor_power_voltage_table[index])
            
            if property['sensor_name'] == 'PSU1_Volt_Out' and GetPsuPresent(1) == 0:
                continue
            if property['sensor_name'] == 'PSU2_Volt_Out' and GetPsuPresent(2) == 0:
                continue
 
            object = bus.get_object(DBUS_NAME, sensor_power_voltage_table[index])

            interface = dbus.Interface(object, DBUS_INTERFACE)

            property['sensor_number']  = interface.Get(SENSOR_HWMON_INTERFACE, 'sensornumber')
            property['upper_critical_threshold']  = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_upper')
            property['lower_critical_threshold']  = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_lower')

            scale = interface.Get(SENSOR_HWMON_INTERFACE, 'scale')
            value = interface.Get(SENSOR_VALUE_INTERFACE, 'value')
            
            property['reading_value'] = value * math.pow(10, scale)
            
            result['Voltages'][str(index)] = property

        #PowerSupplies
        for index in range(0, MAX_PSU_NUM):
            if GetPsuPresent(index+1) == 1:
                object = bus.get_object(DBUS_NAME, sensor_power_powersupplies_table[index])
                interface = dbus.Interface(object, DBUS_INTERFACE)
                
                psu_name = 'psu' + str(index+1)

                result[psu_name + '_power_capacity'] = interface.Get(SENSOR_VALUE_INTERFACE, 'value')
                result[psu_name + '_power_output_watt'] = ''

                dbusctl = obmc_dbuslib.ObmcRedfishProviders()
                manufacture_data = dbusctl.get_fru_info('POWERSUPPLYUNIT'+str(index+1))

                result[psu_name + '_model_number'] = manufacture_data['model_number']
                result[psu_name + '_serial_number'] = manufacture_data['serial_number']
                result[psu_name + '_manufacturer_name'] = ''
                result[psu_name + '_serial_number'] = ''
                result[psu_name + '_part_number'] = ''

    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    result[completion_code.cc_key] = completion_code.success
    
    return result
   