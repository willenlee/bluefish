#**************************************************************
#*                                                            *
#*   Copyright (C) Microsoft Corporation. All rights reserved.*
#*                                                            *
#**************************************************************

import dbus
import dbus.service
import collections
import obmc_dbuslib
import sys

sys.path.append ("/usr/sbin")
import exp_lib

from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
from utils import completion_code

bus = get_dbus()
exp = exp_lib.expander()

MAX_EXPANDER_DRIVES = 22

def string_to_int(input_data):
        temp = [input_data[x:x+3] for x in xrange(0, len(input_data), 3)]
        output_data = [int(temp[x],16) for x in range(0,len(temp))]
        return output_data

def get_id_led_state(expander_id): #TBD
    result = {}

    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        pydata = dbusctl.power_control('state')

    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    if(int(pydata) == 0):
        result['id_led'] = 'Off'
    else:
        result['id_led'] = 'On'

    result[completion_code.cc_key] = completion_code.success

    return result

def get_expander_fru(expander_id): #TBD
    result = {}

    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        pydata = dbusctl.get_chassis_info('MAIN_PLANAR')

    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)
    
    result['SE_ID'] = expander_id
    result['manufacturer'] = 'Microsoft'
    result['model_name'] = 'N/A'
    result[completion_code.cc_key] = completion_code.success

    return result
 
def get_expander_drive_status(expander_id, drive_id):

    expander_drive_status = [-1]*MAX_EXPANDER_DRIVES
    expander_drive_link_speed = [-1]*MAX_EXPANDER_DRIVES
    
    result = {}
    
    try:
        output = exp.GetDriveStatus(expander_id-1)

        if(output == "Error"):
            print "Expander %d - NON-ACK!" %(expander_id)
            return set_failure_dict(('Exception:', e), completion_code.failure)
        else:
            data = string_to_int(output)
        
        # The return raw data bytes should not exceed max 46 bytes
        if(len(data) < 3 or data[0] != 0x00 or data[1] > MAX_EXPANDER_DRIVES or len(data) > (2+MAX_EXPANDER_DRIVES*2)):
            print "Expander %d - GetDriveStatus() error!" %(expander_id)
            return set_failure_dict(('Exception:', e), completion_code.failure)
        
        print ' '.join([hex(i) for i in data])

        for index in range(0, data[1]):
            print "0x%x 0x%x" %(data[2+index*2], data[3+index*2])
            id = data[2+index*2]
            status = (data[3+index*2] & 0xF0) >> 4
            speed = data[3+index*2] & 0x0F
            
            expander_drive_status[id-1]= status
            expander_drive_link_speed[id-1] = speed
            
            print "%d %d" %(status, speed)
        
    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)
    
    result['SE_ID'] = expander_id
    result['DRIVE_ID'] = drive_id
    result['drive_id_led'] = 'N/A'
    result['drive_revision'] = 'N/A'
    result['drive_status'] = 'N/A'
    result['drive_speed'] = 'N/A'
    
    if(expander_drive_status[drive_id-1] == 0):
        result['drive_status'] = 'Failed'
    elif(expander_drive_status[drive_id-1] == 1):
        result['drive_status'] = 'Ready'

    if(expander_drive_link_speed[drive_id-1] == 0):
        result['drive_speed'] = '1.5G'
    elif(expander_drive_link_speed[drive_id-1] == 1):
        result['drive_speed'] = '3.0G'
    elif(expander_drive_link_speed[drive_id-1] == 2):
        result['drive_speed'] = '6.0G'
    elif(expander_drive_link_speed[drive_id-1] == 3):
        result['drive_speed'] = '12.0G'
        
    result[completion_code.cc_key] = completion_code.success

    return result

def set_expander_drive_power(expander_id, drive_id, state):

    try:
        output = exp.SetPowerControl(expander_id-1, drive_id, state)
        if(output == "Error"):
            print "Expander %d - NON-ACK!" %(expander_id)
            return set_failure_dict(('Exception:', e), completion_code.failure)
        else:
            data = string_to_int(output)

        if(data[0] != 0x00):
            print "Expander %d - SetPowerControl() error!" %(expander_id)
            return set_failure_dict(('Exception:', e), completion_code.failure)

    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)
 
    result = {}
    result[completion_code.cc_key] = completion_code.success

    return result
