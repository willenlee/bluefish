import os
import dbus
import dbus.service
import collections

from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
from utils import completion_code

bus = get_dbus()

EVENT_LOG_PATH = '/var/lib/obmc/events/'

DBUS_SERVICE_NAME = 'org.openbmc.records.events'
DBUS_OBJECT_PATH = '/org/openbmc/records/events'
DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'

DBUS_EVENT_LOG_INTERFACE = 'org.openbmc.recordlog'
DBUS_EVENT_LOG_PROPERTY_INTERFACE = 'org.openbmc.record'

def clear_event_log():
    object = bus.get_object(DBUS_SERVICE_NAME, DBUS_OBJECT_PATH)
    interface = dbus.Interface(object, DBUS_EVENT_LOG_INTERFACE)

    interface.clear("")
    
    print("Clear all event log!")
    
    result = {}
    result[completion_code.cc_key] = completion_code.success

    return result

def get_event_log(log_id):
    event_log_object_path = DBUS_OBJECT_PATH + "/" + log_id

    try:
        object = bus.get_object(DBUS_SERVICE_NAME, event_log_object_path)
        interface = dbus.Interface(object, DBUS_INTERFACE)

        result = interface.GetAll(DBUS_EVENT_LOG_PROPERTY_INTERFACE)

        #print "Get event log ", log_id, "\n", result
        #print "\n".join(("%s: %s" % (k, result[k]) for k in result))
    
    except Exception, e:
        print "!!! DBus error !!!\n"
            
    for property_name in result:
        if property_name == 'time':
            date_time = result[property_name]
        if property_name == 'message':
            message = result[property_name]
        if property_name == 'severity':
            severity = result[property_name]
        if property_name == 'expander_index':
            expander_index = result[property_name]
        if property_name == 'sensor_type':
            sensor_type = result[property_name]
        if property_name == 'sensor_number':
            sensor_number = result[property_name]
    
    result = {}
    result['Id'] = log_id
    result['ExpanderIndex'] = str(expander_index)
    result['Severity'] = str(severity)
    result['Created'] = str(date_time)
    result['SensorType'] = str(sensor_type)
    result['SensorNumber'] = str(sensor_number)
    result['Message'] = str(message)
    
    return result
    
def get_event_log_count():
    for root, dirs, files in os.walk(EVENT_LOG_PATH):
        event_log_count = len(files)
    
    return event_log_count
    
def get_event_log_all():
    result = {}
    result['members'] = collections.OrderedDict()
 
    for root, dirs, files in os.walk(EVENT_LOG_PATH):
        event_log_count = len(files)

    event_log_count += 1

    for index in range(1, event_log_count):
        entry = get_event_log(str(index))
        result['members'][str(index)] = entry
    return result 
 
