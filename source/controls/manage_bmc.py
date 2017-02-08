#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
import lib_utils
import collections
import obmc_dbuslib

from ctypes import *
from manage_network import *
from manage_fwversion import *
from collections import OrderedDict


def set_bmc_warm_reset(action):
    result = {}
    if action.upper() == 'WARMRESET':
        op = 'WarmReset'
    else:
        return set_failure_dict("Unknown parameter", completion_code.failure)
    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        dbusctl.bmc_reset_operation(str(op))
    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    return set_success_dict(result)
def set_bmc_fwupdate(action):
    result = {}
    if action.upper() == 'PREPARE':
        op = 'Prepare'
    elif action.upper() == 'APPLY':
        op = 'Apply'
    elif action.upper() == 'ABORT':
        op = 'Abort'
    else:
        return set_failure_dict("Unknown parameter", completion_code.failure)
    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        dbusctl.fw_update_operation(str(op))
    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    return set_success_dict(result)

def get_bmc_fwupdate_state(action):
    result = {}

    if action.upper() == 'QUERY':
        op = 'Query'
        try:
            dbusctl = obmc_dbuslib.ObmcRedfishProviders()
            pydata = dbusctl.fw_update_operation(str(op))
            newdata = pydata.replace('\n', '  ')
        except Exception, e:
            return set_failure_dict(('Exception:', e), completion_code.failure)
    else:
        return set_failure_dict("Unknown parameter", completion_code.failure)
    result["UPDATE_PROGRESS"] = newdata
    result[completion_code.cc_key] = completion_code.success
    return result


def show_rack_manager_hostname():
    result = {}
    
    result["Hostname"] = socket.gethostname()
    result[completion_code.cc_key] = completion_code.success

    return result




def set_bmc_attention_led(setting):
    result = {}
    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        dbusctl.led_operation(str(setting), 'identify')
    
    except Exception,e:
        return set_failure_dict(('Exception:', e),completion_code.failure)

    return set_success_dict(result)

def get_bmc_attention_led_status():
    result = {}

    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        pydata = dbusctl.led_operation('state', 'identify')

    except Exception,e:
        return set_failure_dict(('Exception:', e),completion_code.failure)
    
    if(pydata == 'Off'):
        result["Chassis_IndicatorLED"] = 'Off'
    elif (pydata == 'Lit'):
        result["Chassis_IndicatorLED"] = 'Lit'
    elif (pydata == 'Blinking'):
        result["Chassis_IndicatorLED"] = 'Blinking'
    else:
        result["Chassis_IndicatorLED"] = 'Unknown'
                
    return set_success_dict(result)

def get_rack_manager_port_status(port_id):
    port_id = int(port_id)

    if port_id == 0:
        result = powerport_get_all_port_status()
    else:
        result = powerport_get_port_status(port_id, "pdu")

    return result

def get_nic(serverid):
    try:
        nic_rsp = {}
        
        nic_rsp["Nic Info"] = {}

        get_nic_info = get_server_nicinfo(serverid)
                                
        if get_nic_info[completion_code.cc_key] == completion_code.success:
            get_nic_info.pop(completion_code.cc_key, None)
            nic_rsp["Nic Info"] = get_nic_info
        else:
            nic_rsp["Nic Info"] = get_nic_info
            
    except Exception, e:
        #log_err("Exception to get server _info ",e)
        return set_failure_dict(("Exception: get nic info ",e), completion_code.failure)
    
    return nic_rsp



def set_hostname (hostname):
    result = {}

    try:
        with open ("/etc/hostname", "w") as config:
            config.write (hostname + "\n")

        subprocess.check_output (["hostname", hostname], stderr = subprocess.STDOUT)
        result[completion_code.cc_key] = completion_code.success

    except CalledProcessError as error:
        result[completion_code.cc_key] = completion_code.failure
        #result["ErrorCode"] = error.returncode
        result[completion_code.desc] = error.output.strip ()

    except Exception as error:
        result[completion_code.cc_key] = completion_code.failure
        result[completion_code.desc] = str (error)

    return result
