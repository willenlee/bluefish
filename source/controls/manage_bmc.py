#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
import lib_utils
import collections

from ctypes import *
from manage_network import *
from manage_fwversion import *
from collections import OrderedDict



def show_rack_manager_hostname():
    result = {}
    
    result["Hostname"] = socket.gethostname()
    result[completion_code.cc_key] = completion_code.success

    return result



def set_rack_manager_fwupdate(filename):
    
    if filename is None or filename == "":
        return set_failure_dict("Update file not provided", completion_code.failure)
    
    result = {}
    output = -1
    
    try:
        fwupdate_binary = lib_utils.get_fwupdate_library ()
        
        output = fwupdate_binary.ocs_fwup_startupgrade(filename)
        
        if output != 0:
            return set_failure_dict("Failed to start FW update using FWUpgrade library: {0}".format(str(output)), completion_code.failure)
            
    except Exception, e:  
        return set_failure_dict(("set_rack_manager_fwupdate() Exception {0}".format(str(e))), completion_code.failure) 
    
    result[completion_code.cc_key] = completion_code.success
        
    return result


def manager_session_list():
    result = {}
    output = dict()
    out = subprocess.check_output("netstat -tnp | grep :22 | grep ESTABLISHED", shell = True)
        
    if out is not None:
        for line in out.splitlines(True):
            sessionid = line.split()[6].split('/')[0]
            clientip = line.split()[4].split(':')[0]
            clientport = line.split()[4].split(':')[1]
            output.setdefault(sessionid, [])
            output[sessionid].append(clientip)
            output[sessionid].append(clientport)
    
    result["session"] = output
    result[completion_code.cc_key] = completion_code.success

    return result

def manager_session_kill(sessionid):
    result = {}
    output = dict()
    cmdstr = "ps | grep sshd | grep %s" % (str(sessionid))
    out = subprocess.check_output(cmdstr, shell = True)
        
    if out is not None:
        cmdstr = "kill -9 %s" % (str(sessionid))
        out = subprocess.check_output(cmdstr, shell = True)    		
    else:
        return set_failure_dict("manager session kill invalid session id{0}".format(e), sessionid)         
        
    result[completion_code.cc_key] = completion_code.success
    return result


def set_rack_manager_attention_led(setting):
    result = {}
    output = -1
        
    if setting != 0 and setting != 1:
        return set_failure_dict(("Unknown setting passed to set_rack_manager_attention_led.: ", setting),completion_code.failure)

    state = c_uint()
    
    try:
        gpio_binary = get_gpio_library ()
            
        output = gpio_binary.ocs_port_attentionled(setting, byref(state))
        
        if output != 0:
            return set_failure_dict(("Failed to set attention led using GPIO library:", output),completion_code.failure)
    
    except Exception,e:              
        return set_failure_dict(('Exception:', e),completion_code.failure)
        
    return set_success_dict(result)

def get_rack_manager_attention_led_status():
    result = {}
    output = -1

    state = c_uint()

    try:
        gpio_binary = get_gpio_library()
            
        output = gpio_binary.ocs_port_attentionled(2, byref(state))
        
        if output != 0:
            return set_failure_dict(("Failed to get attention led state using GPIO library:", output), completion_code.failure)

    except Exception,e:   
        return set_failure_dict(('Exception:', e),completion_code.failure)
    
    if(state.value == 0):
        result["Manager LED Status"] = 'OFF'
    elif (state.value == 1):
        result["Manager LED Status"] = 'ON'
    else:
        result["Manager LED Status"] = 'Unknown'
                
    return set_success_dict(result)

def get_rack_manager_port_status(port_id):
    port_id = int(port_id)

    if port_id == 0:
        result = powerport_get_all_port_status()
    else:
        result = powerport_get_port_status(port_id, "pdu")

    return result
        
def get_power_supply_objects():
    class HscStatus(LittleEndianStructure):
          _fields_ = [('noFaults', c_byte, 1),
                      ('cml_fault', c_byte, 1),
                      ('temperature_fault', c_byte, 1),
                      ('vin_uv_fault', c_byte, 1),
                      ('iout_oc_fault', c_byte, 1),
                      ('vout_ov_fault', c_byte, 1),
                      ('unit_off', c_byte, 1),
                      ('unit_busy', c_byte, 1),
                      ('unknown_fault', c_byte, 1),
                      ('other_fault', c_byte, 1),
                      ('fan_fault', c_byte, 1),
                      ('power_good', c_byte, 1),
                      ('mfr_fault', c_byte, 1),
                      ('input_fault', c_byte, 1),
                      ('iout_pout_fault', c_byte, 1),
                      ('vout_fault', c_byte, 1)]
    
    hscstatus_str = ""
      
    try:
        completionstate = completion_code.success
        result = {}
        
        input_voltage = c_double()
        power = c_double()
        
        hsc_binary = lib_utils.get_hsc_library ()
        
        hscstatus = HscStatus(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

        power_output = hsc_binary.hsc_get_power(byref(power))
        
        input_output = hsc_binary.hsc_get_inputvoltage(byref(input_voltage))
        
        status_output = hsc_binary.hsc_get_status(byref(hscstatus))
        
        if power_output == 0:
            result["HSC Power"] = round(power.value,2)
        else:
            completionstate = completion_code.failure
        
        if input_output == 0:
            result["HSC Input-Voltage"] = round(input_voltage.value,2)
        else:
            completionstate = completion_code.failure
        
        if status_output == 0:
            if hscstatus.power_good == 1:
                result["HSC Status"] = "OK" + '{' + str(hscstatus.power_good) + '}'
            else:
                result["HSC Status"] = "Alert" + '{' + str(hscstatus.power_good) + '}'
        else:
            completionstate = completion_code.failure
            
    except Exception,e:   
        return set_failure_dict(("Exception:", e),completion_code.failure)
    
    result[completion_code.cc_key] = completionstate
    return result

def get_sensor_objects():
    result = {}

    temperature = c_double()
    humidity = c_double()
    
    try:
        hdc_binary = lib_utils.get_hdc_library ()

        temperature_output = hdc_binary.hdc_get_temperature(byref(temperature))
        humidity_output = hdc_binary.hdc_get_humidity(byref(humidity))
        
        if temperature_output == 0 and humidity_output == 0:
            result[completion_code.cc_key] = completion_code.success           
        else:
            result[completion_code.cc_key] = completion_code.failure
            
        result["Temperature"] = round(temperature.value, 2)
        result["Humidity"] = round(humidity.value,2)
            
    except Exception,e:   
        return set_failure_dict(("Exception:", e),completion_code.failure)

    return result

def get_sensor_objects_with_units ():
    result = get_sensor_objects ()
    if (result[completion_code.cc_key] == completion_code.success):
        result["Temperature"] = str (result["Temperature"]) + " C"
        result["Humidity"] = str (result["Humidity"]) + " RH"
        
    return result

def get_rm_health(mode):
    completionstate = True
    try:   
        rm_health_rsp = {}
        #rm_health_rsp["Manager"] = {}
        rm_health_rsp["PSU Health"] = {}   
        rm_health_rsp["Sensor Reading"] = {}
        rm_health_rsp["Memory Usage"] = {}
        rm_health_rsp["Server State"] = {}
        
        current_time = None
        up_time = None
        
        # Blade Health
        blade_health = server_info(mode)
        if completion_code.cc_key in blade_health.keys():
            if blade_health[completion_code.cc_key] == completion_code.success:
                blade_health.pop(completion_code.cc_key,None)
                rm_health_rsp["Server State"] = blade_health
            else:
                blade_health.pop(completion_code.cc_key,None)
                completionstate &= False
                rm_health_rsp["Server State"] = blade_health
        else:
            completionstate &= False
            rm_health_rsp["Server State"] = blade_health
        
        led_status = get_rack_manager_attention_led_status()        
        if completion_code.cc_key in led_status.keys() and (led_status[completion_code.cc_key] == completion_code.success):
            rm_health_rsp["LED Status"] = led_status["Manager LED Status"]
        else:
            completionstate &= False
            rm_health_rsp["LED Status"] = ''
            
        rm_time = get_rm_uptime()
        if completion_code.cc_key in rm_time.keys():
            if rm_time[completion_code.cc_key] == completion_code.failure:
                completionstate &= False
            
            if 'Current Time' in rm_time.keys():
                current_time = rm_time["Current Time"].strip()
            
            if 'Up Time' in rm_time.keys():
                up_time = rm_time["Up Time"].strip()
                
            rm_health_rsp["Current Time"] = current_time
            rm_health_rsp["Manager Uptime"] = up_time
        else:
            completionstate &= False
            rm_health_rsp["Current Time"] = completion_code.failure
            rm_health_rsp["Manager Uptime"] = completion_code.failure
        
          
        rm_memory = get_memory_details()        
        if completion_code.cc_key in rm_memory.keys():        
            if(rm_memory[completion_code.cc_key] == completion_code.success):
                rm_memory.pop(completion_code.cc_key,None)
                rm_health_rsp["Memory Usage"] = rm_memory
            else:
                rm_memory.pop(completion_code.cc_key,None)
                completionstate &= False
                rm_health_rsp["Memory Usage"][completion_code.cc_key]= completion_code.failure
        else:
            completionstate &= False
            rm_health_rsp["Memory Usage"][completion_code.cc_key]= completion_code.failure
            
            
        psu_health = get_power_supply_objects()        
        if completion_code.cc_key in psu_health.keys():
            if(psu_health[completion_code.cc_key] == completion_code.success):
                psu_health.pop(completion_code.cc_key,None)
                rm_health_rsp["PSU Health"] = psu_health
            else:
                psu_health.pop(completion_code.cc_key,None)
                completionstate &= False
                rm_health_rsp["PSU Health"][completion_code.cc_key] = completion_code.failure
        else:
            completionstate &= False
            rm_health_rsp["PSU Health"][completion_code.cc_key] = completion_code.failure
            
        
        sensor_reading = get_sensor_objects_with_units()
        if completion_code.cc_key in sensor_reading.keys():    
            if(sensor_reading[completion_code.cc_key] == completion_code.success):
                sensor_reading.pop(completion_code.cc_key,None)           
                rm_health_rsp["Sensor Reading"] = sensor_reading
            else:
                sensor_reading.pop(completion_code.cc_key,None) 
                completionstate &= False
                rm_health_rsp["Sensor Reading"][completion_code.cc_key] = completion_code.failure
        else:
            completionstate &= False
            rm_health_rsp["Sensor Reading"][completion_code.cc_key] = completion_code.failure
    
    except Exception, e:
        #log.exception("Exception error is: %s " %e)
        rm_health_rsp[completion_code.cc_key] = completion_code.failure
        rm_health_rsp[completion_code.desc] = "Get manager health Exception: ", e
        return rm_health_rsp
    
    
    if completionstate:
        rm_health_rsp[completion_code.cc_key] = completion_code.success
    else:
        rm_health_rsp[completion_code.cc_key] = completion_code.failure
    
    return rm_health_rsp

def read_fru(boardtype):
    fru_util_exe_cmd = None

    try:
        if boardtype == "rm_mb" or boardtype == "row_mb":
            fru_util_exe_cmd = "/usr/bin/ocs-fru -c 0 -s 50 -r"
        elif boardtype == "rm_pib":
            fru_util_exe_cmd = "/usr/bin/ocs-fru -c 1 -s 51 -r"
        elif boardtype == "rm_acdc":
            fru_util_exe_cmd = "/usr/bin/ocs-fru -c 1 -s 50 -r"
        elif boardtype == "row_pib":
            fru_util_exe_cmd = "/usr/bin/ocs-fru -c 1 -s 52 -r"  
        
        if fru_util_exe_cmd:
            fru_response = parse_read_fru(fru_util_exe_cmd)
            
            if fru_response is None or not fru_response: # Check empty or none
                #log.error(": failed to read fru data: %s" %boardtype)
                fru_response[completion_code.cc_key] = completion_code.failure
                fru_response[completion_code.desc] = "Fru response is empty"
        else:
            return set_failure_dict ("Unknown board type {0}".format (boardtype),
                completion_code.failure)
        
    except Exception,e:
            return set_failure_dict(e, completion_code.failure)    
    
    return fru_response 

def write_fru(boardtype, filepath):
    fru_util_exe_cmd = None
    try:
        if boardtype == "rm_mb" or boardtype == "row_mb":
            fru_util_exe_cmd = "/usr/bin/ocs-fru -c 0 -s 50 -w" + ' ' + filepath
        elif boardtype == "rm_pib":
            fru_util_exe_cmd = "/usr/bin/ocs-fru -c 1 -s 51 -w" + ' ' + filepath
        elif boardtype == "rm_acdc":
            fru_util_exe_cmd = "/usr/bin/ocs-fru -c 1 -s 50 -w" + ' ' + filepath
        elif boardtype == "row_pib":
            fru_util_exe_cmd = "/usr/bin/ocs-fru -c 1 -s 52 -w" + ' ' + filepath 
        
        if fru_util_exe_cmd:
            fru_response = parse_write_fru(fru_util_exe_cmd)
            
            if fru_response is None or not fru_response: # Check empty or none
                #log.error(": failed to read fru data: %s" %boardtype)
                fru_response[completion_code.cc_key] = completion_code.failure
                fru_response[completion_code.desc] = "Fru response is empty"
        else:
            return set_failure_dict ("Unknown board type {0}".format (boardtype),
                completion_code.failure)
        
    except Exception,e:
            return set_failure_dict(("Exception",e), completion_code.failure)    
    
    return fru_response

def get_rack_manager_info(rmmode): 
    completioncode = completion_code.success
    try:  
        manager_rsp = {}
        manager_rsp["Server Info"] = {}  
        manager_rsp["RM Controller"] = {}   
        manager_rsp["PSU Info"] = {}
        
        manager_rsp["Type"] =  (rmmode + " manager").upper()  
        
        rm_time = get_rm_uptime()
        if rm_time[completion_code.cc_key] == completion_code.failure:
            completioncode = completion_code.failure            
        
        if 'Current Time' in rm_time.keys():
            current_time = rm_time["Current Time"].strip()
        
        if 'Up Time' in rm_time.keys():
            up_time = rm_time["Up Time"].strip()
            
        manager_rsp["Current Time"] = current_time
        manager_rsp["Manager Uptime"] = up_time
        
        manager_controller = manager_info()
        # Rack Manager Controller
        if(manager_controller[completion_code.cc_key] == completion_code.success):
            manager_controller.pop(completion_code.cc_key,None)
            manager_rsp["RM Controller"] = manager_controller            
        else:
            manager_controller.pop(completion_code.cc_key,None)
            completioncode = completion_code.failure
            manager_rsp["RM Controller"] = manager_controller
            
        # Server Information
        blade_info = server_info(rmmode, True)
        if blade_info[completion_code.cc_key] == completion_code.success:
            blade_info.pop(completion_code.cc_key,None)
            manager_rsp["Server Info"] = blade_info
        else:
            blade_info.pop(completion_code.cc_key,None)
            completioncode = completion_code.failure
            manager_rsp["Server Info"] = blade_info
            
        #PSU Information
        psu_info = get_power_supply_objects()
        if psu_info[completion_code.cc_key] == completion_code.success:
            psu_info.pop(completion_code.cc_key,None)
            manager_rsp["PSU Info"] = psu_info
        else:
            psu_info.pop(completion_code.cc_key,None)
            completioncode = completion_code.failure
            manager_rsp["PSU Info"] = psu_info
         
    except Exception,e:
            return set_failure_dict(("Exception",e), completion_code.failure)    
    
    manager_rsp[completion_code.cc_key] = completioncode 
    return manager_rsp

def call_fru_util(command):
    try:    
        popencmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True);

        output, error = popencmd.communicate()
        
        p_status = popencmd.wait();
        
        return  {'status_code':p_status, 'stdout':output, 'stderr': error}
    except Exception:
        return set_failure_dict("Subprocess ocs-fru call exception, Command: " + command, "-1")

def manager_info():
    completionstate = True
    current_time = ""
    up_time = ""
    try:
        rm_controller = {}
        
        rm_controller["Name"] = socket.gethostname ()
        rm_controller["Asset Info"] = {}
        rm_controller["Network"] = {}
        rm_controller["Status"] = {}
        rm_controller["Temperature"] = {}
        
        led_rsp = get_rack_manager_attention_led_status()
        led_status = ''
                
        if(led_rsp[completion_code.cc_key] == completion_code.success):
            led_status = led_rsp["Manager LED Status"]
        else:
            led_status = completion_code.failure
            completionstate &= False
            
        rm_controller["Status"]["LED Status"] =  led_status              
       
        rm_controller["Status"]["Power"] = "ON"
        rm_controller["Status"]["Health"] = "OK"
        
        fw_version = get_ocsfwversion()
        
        if completion_code.cc_key in fw_version.keys():
            if (fw_version[completion_code.cc_key] == completion_code.success):
                rm_controller["FW Version"] = fw_version['Package']
            else:
                rm_controller["FW Version"] = completion_code.failure
                completionstate &= False
        
        
        ip_address = get_ip_address("eth0")
        macaddress = get_macsocket("eth0")
        
        if ip_address is None or not ip_address:
            completionstate &= False
            rm_controller["Network"]["IP Address"] = completion_code.failure
        else:                
            rm_controller["Network"]["IP Address"] = ip_address
            
        if macaddress is None or not macaddress:
            completionstate &= False
            rm_controller["Network"]["Mac Address"] = completion_code.failure
        else:
            rm_controller["Network"]["Mac Address"] = macaddress
            
        sensor_reading = get_sensor_objects_with_units()
        
        if(sensor_reading[completion_code.cc_key] == completion_code.success):
            sensor_reading.pop(completion_code.cc_key,None)           
            rm_controller["Temperature"]["Temperature"] = sensor_reading["Temperature"]
            rm_controller["Temperature"]["Humidity"] = sensor_reading["Humidity"]            
        else:
            completionstate &= False
            rm_controller["Temperature"]["Temperature"] = completion_code.failure
            rm_controller["Temperature"]["Humidity"] = completion_code.failure
            
        fru = fru_Info()

        if fru is None or not fru:
            completionstate &= False
            rm_controller["Asset Info"] = "Fru response is empty"
        else:
            if(fru[completion_code.cc_key] == completion_code.success):
                fru.pop(completion_code.cc_key,None)
                rm_controller["Asset Info"] = fru
            else:
                completionstate &= False
                        
    except Exception,e:
        #print (Exception inof, e)
        return set_failure_dict(("Rm Controller exception",e), completion_code.failure)
    
    if completionstate:
        rm_controller[completion_code.cc_key] = completion_code.success
    else:
        rm_controller[completion_code.cc_key] = completion_code.failure
                    
    return rm_controller

def fru_Info():    
    try:    
        interface = "/usr/bin/ocs-fru -c 0 -s 50 -r"
        
        output = call_fru_util(interface)  

        rack_rsp = {}
        
        if(output['status_code'] == 0):      
                #log.info("Completion Code: %s"%Config.completioncode[0])
                sdata = output['stdout'].split('\n')                                
                    
                for value in sdata:                    
                # FRU details
                    if "product productname" in value:
                        rack_rsp["Name"]=  value.split(":")[-1].strip()
                                                
                    elif "product manufacture" in value:
                        rack_rsp["Manufacturer"]=  value.split(":")[-1].strip()
                                            
                    elif "product productversion" in value:
                        rack_rsp["Firmware Version"]=  value.split(":")[-1].strip()
                        
                    elif "board version" in value:
                        rack_rsp["Hardware Version"] = value.split(":")[-1].strip()
                    
                    elif "product serial" in value:
                        rack_rsp["SerialNumber"] = value.split(":")[-1].strip()
                        
                    elif "product fruid" in value:
                        rack_rsp["FruId"] = value.split(":")[-1].strip()              
                
                    elif "product assettag: " in value:
                        rack_rsp["AssetTag"] = value.split(":")[-1].strip()
                        
                    elif "product build" in value:
                        rack_rsp["Build"] = value.split(":")[-1].strip()  
                
                rack_rsp[completion_code.cc_key] = completion_code.success
        else:   
            errorData = output['stderr'].split('\n')            
            rack_rsp[completion_code.cc_key] = completion_code.failure
            
            for data in errorData:
                if "Error" in data:
                    rack_rsp[completion_code.desc] = data.split(":")[-1]
                elif "Completion Code" in data:
                    rack_rsp["Error Code"] = data.split(":")[-1]         
         
                              
    except Exception, e:         
        return set_failure_dict(("Manager info parse results() Exception: ",e), completion_code.failure)    
    
    return rack_rsp  

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
        
def parse_read_fru(frucommand):
    try:        
        output = call_fru_util(frucommand)   
        
        fru_rsp = {}

        if(output['status_code'] == 0):
                fru_rsp[completion_code.cc_key] = completion_code.success
                #log.info("Completion Code: %s"%Config.completioncode[0])
                sdata = output['stdout'].split('\n')                                
                
                for value in sdata:           
                    #Board Info Area       
                    if "board mfgdatetime" in value:
                        fru_rsp["Board Manufacturer Date"]= value.split(":")[-1].strip()                         
                    elif "board manufacturer" in value:
                        fru_rsp["Board Manufacturer"]=  value.split(":")[-1].strip()                                              
                    elif "board name" in value:
                        fru_rsp["Board Name"]=  value.split(":")[-1].strip()                           
                    elif "board serial" in value:
                        fru_rsp["Board Serial"] = value.split(":")[-1].strip() 
                    elif "board part" in value:
                        fru_rsp["Board Part Number"] = value.split(":")[-1].strip()  
                    elif "board fruId" in value:
                        fru_rsp["Board Fru Id"] = value.split(":")[-1].strip()  
                    elif "board address1" in value:
                        fru_rsp["Board Address1"] = value.split(":")[-1].strip() 
                    elif "board address2" in value:
                        fru_rsp["Board Address2"] = value.split(":")[-1].strip()            
                    elif "board version" in value:
                        fru_rsp["Board Version"] = value.split(":")[-1].strip()  
                    elif "board build" in value:
                        fru_rsp["Board Build"] = value.split(":")[-1].strip()  
                    #Product Info area   
                    elif "product manufacture" in value:
                        fru_rsp["Product Manufacturer"]=  value.split(":")[-1].strip()                                              
                    elif "product productname" in value:
                        fru_rsp["Product Name"]=  value.split(":")[-1].strip()    
                    elif "product productversion" in value:
                        fru_rsp["Product Version"] = value.split(":")[-1].strip()
                    elif "product assettag" in value:
                        fru_rsp["Product Assettag"] = value.split(":")[-1].strip()                       
                    elif "product serial" in value:
                        fru_rsp["Product Serial"] = value.split(":")[-1].strip() 
                    elif "product fruid" in value:
                        fru_rsp["Product Fru Id"] = value.split(":")[-1].strip()  
                    elif "product subproduct" in value:
                        fru_rsp["Product Subproduct"] = value.split(":")[-1].strip()  
                    elif "product build" in value:
                        fru_rsp["Product Build"] = value.split(":")[-1].strip()                                          
        else:   
            error_data = output['stderr'].split('\n')    
            error_data = filter(None, error_data)     
            #log_error("Failed to read fru %s ",error_data )   
            fru_rsp[completion_code.cc_key] = completion_code.failure
            
            for data in error_data:
                if "ERROR" in data:
                    fru_rsp[completion_code.cc_key] = data
                elif "eeprom read completion code" in data:
                    fru_rsp["Utility Completion Code"] = data.split(":")[-1]  
                elif "not found" in data:                           
                    fru_rsp["stderr"] = error_data 
                    break          
          
    except Exception, e:         
        return set_failure_dict(("parse_read_fru exception:",e) ,completion_code.failure)  
    
    return fru_rsp

def parse_write_fru(frucommand):
    try:        
        output = call_fru_util(frucommand)  
        
        fru_rsp = {}
            
        if(output['status_code'] == 0):
                #log.info("Completion Code: %s"%Config.completioncode[0])
                fru_rsp[completion_code.cc_key] = completion_code.success                              
                
        else:   
            error_data = output['stderr'].split('\n')    
            error_data = filter(None, error_data)     
            #log_error("Failed to read fru %s ",error_data )   
            fru_rsp[completion_code.cc_key] = completion_code.failure
            
            for data in error_data:
                if "ERROR" in data:
                    fru_rsp[completion_code.desc] = data
                elif "write completion code" in data:
                    fru_rsp["Utility Completion Code"] = data.split(":")[-1]  
                elif "not found" in data:                           
                    fru_rsp["stderr"] = error_data 
                    break                                        
          
    except Exception, e:         
        return set_failure_dict(("parse_write_fru exception:",e) , completion_code.failure)  
    
    return fru_rsp

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
