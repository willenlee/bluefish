#**************************************************************
#*                                                            *
#*   Copyright (C) Microsoft Corporation. All rights reserved.*
#*                                                            *
#**************************************************************

import dbus
import dbus.service
import collections

from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
from utils import completion_code

DBUS_NAME = 'org.openbmc.Sensors'
DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'

SENSOR_VALUE_INTERFACE = 'org.openbmc.SensorValue'
SENSOR_THRESHOLD_INTERFACE = 'org.openbmc.SensorThresholds'
SENSOR_HWMON_INTERFACE = 'org.openbmc.HwmonSensor'

bus = get_dbus()

sensor_mainboard_temperature_table =\
[\
    "/org/openbmc/sensors/temperature/Main_Board_Temp",\
    "/org/openbmc/sensors/Fans/Fan_HSC_Temp"\
]

sensor_fan_speed_table =\
[\
    "/org/openbmc/sensors/speed/fan1",\
    "/org/openbmc/sensors/speed/fan2",\
    "/org/openbmc/sensors/speed/fan3",\
    "/org/openbmc/sensors/speed/fan4"\
]

sensor_fan_temperature_table =\
[\
    "/org/openbmc/sensors/Thermal/Fans/1",\
    "/org/openbmc/sensors/Thermal/Fans/2",\
    "/org/openbmc/sensors/Thermal/Fans/3",\
    "/org/openbmc/sensors/Thermal/Fans/4",\
    "/org/openbmc/sensors/Thermal/Fans/5",\
    "/org/openbmc/sensors/Thermal/Fans/6",\
    "/org/openbmc/sensors/Thermal/Fans/7",\
    "/org/openbmc/sensors/Thermal/Fans/8"\
]

sensor_fan_table =\
[\
    "/org/openbmc/sensors/Fans/Fan_HSC_Power_Out",\
    "/org/openbmc/sensors/Fans/Fan_HSC_Volt_Out"\
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
            property['value'] = 0
            property['upper_critical_threshold'] = 0
        
            object = bus.get_object(DBUS_NAME, sensor_mainboard_temperature_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            properties = interface.GetAll(SENSOR_VALUE_INTERFACE)
            for property_name in properties:
                if property_name == 'value':
                    property['value'] = str(int(properties['value'])/1000)

            properties = interface.GetAll(SENSOR_THRESHOLD_INTERFACE)
            for property_name in properties:
                if property_name == 'critical_upper':
                    property['upper_critical_threshold'] = str(properties['critical_upper'])

            properties = interface.GetAll(SENSOR_HWMON_INTERFACE)
            for property_name in properties:
                if property_name == 'sensornumber':
                    property['sensor_number'] = str(properties['sensornumber'])
        
            result['temperatures'][str(index)] = property

        for index in range(0, len(sensor_fan_temperature_table)):
            property = {}
            property['sensor_id'] = index+1
            property['sensor_number'] = 0
            property['upper_critical_threshold'] = 0
            property['value'] = 0
            property['PWM'] = 0

            object = bus.get_object(DBUS_NAME, sensor_fan_speed_table[index/2])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            properties = interface.GetAll(SENSOR_VALUE_INTERFACE)
            for property_name in properties:
                if property_name == 'value':
                    property['PWM'] = str(properties['value'])

            object = bus.get_object(DBUS_NAME, sensor_fan_temperature_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            properties = interface.GetAll(SENSOR_VALUE_INTERFACE)
            for property_name in properties:
                if property_name == 'value':
                    property['value'] = str(properties['value'])
            
            properties = interface.GetAll(SENSOR_THRESHOLD_INTERFACE)
            for property_name in properties:
                if property_name == 'critical_upper':
                    property['upper_critical_threshold'] = str(properties['critical_upper'])
            
            properties = interface.GetAll(SENSOR_HWMON_INTERFACE)
            for property_name in properties:
                if property_name == 'sensornumber':
                    property['sensor_number'] = str(properties['sensornumber'])
                   
            result['fans'][str(index)] = property
            
    except Exception, e:
        print "!!! DBus error !!!\n"
            
    return result
