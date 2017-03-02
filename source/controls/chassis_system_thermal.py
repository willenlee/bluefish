#**************************************************************
#*                                                            *
#*   Copyright (C) Microsoft Corporation. All rights reserved.*
#*                                                            *
#**************************************************************

import dbus
import dbus.service
import collections
import math

from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
from utils import completion_code

DBUS_NAME = 'org.openbmc.Sensors'
DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'

SENSOR_VALUE_INTERFACE = 'org.openbmc.SensorValue'
SENSOR_THRESHOLD_INTERFACE = 'org.openbmc.SensorThresholds'
SENSOR_HWMON_INTERFACE = 'org.openbmc.HwmonSensor'

bus = get_dbus()

def get_sensor_name(sensor_path):
    path_list = sensor_path.split("/")
    return path_list[-1]

sensor_mainboard_temperature_table =\
[\
    "/org/openbmc/sensors/temperature/Main_Board_Temp",\
    "/org/openbmc/sensors/Fans/Fan_HSC_Temp",\
    "/org/openbmc/sensors/temperature/PDB_Temp"\
]

sensor_fan_pwm_table =\
[\
    "/org/openbmc/sensors/speed/Fan_PWM_1",\
    "/org/openbmc/sensors/speed/Fan_PWM_2",\
    "/org/openbmc/sensors/speed/Fan_PWM_3",\
    "/org/openbmc/sensors/speed/Fan_PWM_4"\
]

sensor_fan_rpm_table =\
[\
    "/org/openbmc/sensors/Thermal/Fans/Fan_RPM_1",\
    "/org/openbmc/sensors/Thermal/Fans/Fan_RPM_2",\
    "/org/openbmc/sensors/Thermal/Fans/Fan_RPM_3",\
    "/org/openbmc/sensors/Thermal/Fans/Fan_RPM_4",\
    "/org/openbmc/sensors/Thermal/Fans/Fan_RPM_5",\
    "/org/openbmc/sensors/Thermal/Fans/Fan_RPM_6",\
    "/org/openbmc/sensors/Thermal/Fans/Fan_RPM_7",\
    "/org/openbmc/sensors/Thermal/Fans/Fan_RPM_8"\
]

def get_chassis_thermal():
    result = {}
    result['temperatures'] = collections.OrderedDict()
    result['fans'] = collections.OrderedDict()

    try:
        for index in range(0, len(sensor_mainboard_temperature_table)):
            property = {}
            property['sensor_id'] = index+1
            property['sensor_number'] = 0
            property['sensor_name'] = get_sensor_name(sensor_mainboard_temperature_table[index])
            property['value'] = 0
            property['upper_critical_threshold'] = 0
                
            object = bus.get_object(DBUS_NAME, sensor_mainboard_temperature_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            scale = interface.Get(SENSOR_HWMON_INTERFACE, 'scale')

            value = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

            property['value'] = value * math.pow(10, scale)

            property['upper_critical_threshold'] = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_upper')

            property['sensor_number'] = interface.Get(SENSOR_HWMON_INTERFACE, 'sensornumber')

            result['temperatures'][str(index)] = property

        for index in range(0, len(sensor_fan_rpm_table)):
            property = {}
            property['sensor_id'] = index+1
            property['sensor_number'] = 0
            property['upper_critical_threshold'] = 0
            property['value'] = 0
            property['PWM'] = 0

            object = bus.get_object(DBUS_NAME, sensor_fan_pwm_table[index/2])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            properties = interface.GetAll(SENSOR_VALUE_INTERFACE)
            property['PWM'] = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

            object = bus.get_object(DBUS_NAME, sensor_fan_rpm_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)
            
            property['value'] = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

            property['upper_critical_threshold'] = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_upper')

            property['sensor_number'] = interface.Get(SENSOR_HWMON_INTERFACE, 'sensornumber')

            result['fans'][str(index)] = property
            
    except Exception, e:
        print "!!! DBus error !!!\n"
            
    return result
