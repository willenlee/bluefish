#**************************************************************
#*                                                            *
#*   Copyright (C) Microsoft Corporation. All rights reserved.*
#*                                                            *
#**************************************************************

import dbus
import dbus.service
import collections
import obmc_dbuslib

from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
from utils import completion_code

bus = get_dbus()

def get_chassis_power_state():
    result = {}

    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        pydata = dbusctl.power_control('state')

    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    if(int(pydata) == 0):
        result['power_state'] = 'Off'
    else:
        result['power_state'] = 'On'

    result[completion_code.cc_key] = completion_code.success

    return result

def get_chassis_fru():
    result = {}

    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        pydata = dbusctl.get_chassis_info('MAIN_PLANAR')

    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    result['manufacturer'] = 'Microsoft'
    result['model_name'] = 'N/A'
    result['part_number'] = pydata['PartNumber']
    result['serial_number'] = pydata['SerialNumber']
    
    result[completion_code.cc_key] = completion_code.success

    return result
    