import authentication
import view_helper
import enums
from bottle import HTTPError, auth_basic
from authentication import pre_check_function_call
from pre_settings import command_name_enum
from controls.utils import set_failure_dict, completion_code

import controls.manage_network
import controls.manage_user
import controls.manage_logentry
import controls.manage_fwversion
import time
import datetime

def execute_get_request_queries (query_list, init_values = dict ()):
    """
    Handler for all get requests to query the system for necessary information.
    
    :param query_list: A list of functions to be called that will provide the information required
    for the request.  Each function is a pair that contains the function to call and dictionary of
    arguments.
    :param init_values: The initial set of response information.
    
    :return A dictionary containing the information for generating the response object.
    """
    
    result = init_values.copy ()
    for query in query_list:
        try:
            query_data = query[0] (**query[1])
            view_helper.append_response_information (result, query_data)
            
        except Exception as error:
            view_helper.append_response_information (
                result, set_failure_dict (str (error), completion_code.failure))
    
    return view_helper.replace_key_spaces (result)



def parse_sensor_list (sensors, convert_reading, convert_number, sensor_type):
    """
    Parse the dictionary list of sensor data and convert it into an array used by the REST template.
    
    :param sensors: The dictionary list of sensor data to parse.  As the sensor data is parsed, the
    information will be removed from this dictionary.
    :param convert_reading: A flag indicating if the sensor reading should be converted to a numeber
    or if the raw string should be retained.
    :param convert_number: A flag indicating if the sensor number string should be converted to an
    integer or if the raw string should be retained.
    :param sensor_type: The type of sensor information being parsed.
    
    :return An array containing the parsed sensor data.
    """
    
    status_key = sensor_type + "_Status"
    number_key = sensor_type + "_Number"
    reading_key = sensor_type + "_Reading"
    
    parsed = [None] * len (sensors)
    for i, sensor in sensors.items ():
        try:
            idx = int (i) - 1
            status = sensor.pop (status_key, None)
            if (status and (status != "ns")):
                sensor["Health"] = enums.Health (status, convert = True)
            
            if (convert_number and (number_key in sensor)):
                sensor[number_key] = int (sensor[number_key][:-1], 16)
                
            if (reading_key in sensor):
                reading = sensor[reading_key]
                if (reading == "Disabled"):
                    sensor["State"] = enums.State ("Disabled")
                    del sensor[reading_key]
                else:
                    sensor["State"] = enums.State ("Enabled")
                    if ((not reading) or (reading == "No Reading")):
                        del sensor[reading_key]
                    elif (convert_reading):
                        reading = view_helper.extract_number (reading)
                        if (reading):
                            sensor[reading_key] = reading
                        else:
                            del sensor[reading_key]
            
            parsed[idx] = sensor
            del sensors[i]
            
        except ValueError:
            pass
            
    return filter (None, parsed)

###################
# Top-Level Redfish
###################
@auth_basic (authentication.validate_user)
def get_redfish_version ():
    return view_helper.return_redfish_resource ("version")

@auth_basic (authentication.validate_user)
def get_service_root ():
    return view_helper.return_redfish_resource ("service_root")

def get_redfish_metadata ():
    return view_helper.return_redfish_resource ("metadata")

@auth_basic (authentication.validate_user)
def get_chassis_root ():
    return view_helper.return_redfish_resource ("chassis_root")

@auth_basic (authentication.validate_user)
def get_managers_root ():
    return view_helper.return_redfish_resource ("managers_root")




#########################
# Chassis components
#########################
@auth_basic (authentication.validate_user)
def get_chassis (slot_id, patch = dict ()):
    query = [
        (controls.manage_bmc.get_bmc_attention_led_status, {})
    ]

    result = execute_get_request_queries(query)
    view_helper.update_and_replace_status_information(result, patch)
    return view_helper.return_redfish_resource ("chassis", values = result)


@auth_basic (authentication.validate_user)
def get_chassis_thermal (slot_id):
    return view_helper.return_redfish_resource ("chassis_thermal")

def get_chassis_thermal_redundancy (slot_id, sensor_id):
    return view_helper.return_redfish_resource ("chassis_thermal_redundancy")

@auth_basic (authentication.validate_user)
def get_chassis_power (slot_id):
    return view_helper.return_redfish_resource ("chassis_power")

@auth_basic (authentication.validate_user)
def get_chassis_power_redundancy (slot_id, psu_id):
    return view_helper.return_redfish_resource ("chassis_power_redundancy")

@auth_basic (authentication.validate_user)
def get_chassis_mainboard (slot_id):
    return view_helper.return_redfish_resource ("chassis_mainboard")

@auth_basic (authentication.validate_user)
def get_chassis_storage_enclosure (slot_id, se_id):
    return view_helper.return_redfish_resource ("chassis_storage_enclosure")

@auth_basic (authentication.validate_user)
def get_chassis_storage_enclosure_storage (slot_id, se_id):
    return view_helper.return_redfish_resource ("chassis_storage_enclosure_storage")

@auth_basic (authentication.validate_user)
def get_chassis_storage_enclosure_power (slot_id, se_id):
    return view_helper.return_redfish_resource ("chassis_storage_enclosure_power")

@auth_basic (authentication.validate_user)
def get_chassis_storage_enclosure_thermal (slot_id, se_id):
    return view_helper.return_redfish_resource ("chassis_storage_enclosure_thermal")

@auth_basic (authentication.validate_user)
def get_chassis_storage_enclosure_drive (slot_id, se_id, dr_id):
    return view_helper.return_redfish_resource ("chassis_storage_enclosure_drive")







#########################
# BMC components
#########################
@auth_basic (authentication.validate_user)
def get_bmc (slot_id, patch = dict ()):
    query = [
        (controls.manage_fwversion.get_ocsfwversion, {})
    ]

    result = execute_get_request_queries(query)
    view_helper.update_and_replace_status_information(result, patch)
    return view_helper.return_redfish_resource ("bmc", values = result)


@auth_basic (authentication.validate_user)
def get_bmc_networkprotocol (slot_id):
    return view_helper.return_redfish_resource ("bmc_networkprotocol")
    
@auth_basic (authentication.validate_user)
def get_bmc_ethernets (slot_id):
#    pre_check_function_call (op_category_enum.get_rackmanager_state)
    
    query = [
        (controls.manage_network.display_cli_interfaces, {})
    ]
    
    result = execute_get_request_queries (query)
        
    return view_helper.return_redfish_resource ("bmc_ethernets", values = result)

@auth_basic (authentication.validate_user)
def get_bmc_ethernet (slot_id, eth, patch = dict ()):
#    if (not patch):
#        pre_check_function_call (op_category_enum.get_rackmanager_state)
    
    query = [
        (controls.manage_network.get_network_mac_address, {"if_name":eth}),
        (controls.manage_network.get_network_ip_address, {"if_name":eth}),
        (controls.manage_network.get_network_subnetmask, {"if_name":eth}),
        (controls.manage_network.get_network_gateway, {}),
        (controls.manage_network.get_network_status, {"if_name":eth})
    ]
    
    result = execute_get_request_queries (query)
    if ("InterfaceStatus" in result):
        result["InterfaceStatus"] = str (enums.State (
            str(result["InterfaceStatus"]), convert = True))
    
    result["Intf"] = eth
    result["Description"] = ("Datacenter" if (eth == "eth0") else "Management") + " Network Connection"

    view_helper.update_and_replace_status_information (result, patch)
    return view_helper.return_redfish_resource ("bmc_ethernet", values = result)

@auth_basic (authentication.validate_user)
def get_bmc_log_services (slot_id):
    return view_helper.return_redfish_resource ("bmc_log_service")

@auth_basic (authentication.validate_user)
def get_bmc_log (slot_id):
    result = {}
    result["DateTime"] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    
    return view_helper.return_redfish_resource ("bmc_log", values = result)  

@auth_basic (authentication.validate_user)
def get_bmc_log_entries (slot_id):
    query = [
        (controls.manage_logentry.get_event_log_all, {})
    ]

    result = execute_get_request_queries (query)
    
    return view_helper.return_redfish_resource ("bmc_log_entries", values = result)
    
@auth_basic (authentication.validate_user)
def get_bmc_log_entry (slot_id, entry):
    query = [
        (controls.manage_logentry.get_event_log, {"log_id": entry})
    ]

    result = execute_get_request_queries (query)
    
    if "Id" not in result:
        raise HTTPError (status = 404)
   
    return view_helper.return_redfish_resource ("bmc_log_entry", values = result)
    
@auth_basic (authentication.validate_user)
def get_bmc_serialinterfaces (slot_id):
    return view_helper.return_redfish_resource ("bmc_serialinterfaces")

@auth_basic (authentication.validate_user)
def get_bmc_serialinterface (slot_id):
    return view_helper.return_redfish_resource ("bmc_serialinterface")




############################
# Account service components
############################
@auth_basic (authentication.validate_user)
def get_account_service ():
    return view_helper.return_redfish_resource ("account_service")

@auth_basic (authentication.validate_user)
def get_accounts ():
    pre_check_function_call (command_name_enum.get_rm_state)
    
    query = [
        (controls.manage_user.user_list_all, {})
    ]
    
    result = execute_get_request_queries (query)
    
    return view_helper.return_redfish_resource ("accounts", values = result)

@auth_basic (authentication.validate_user)
def get_account (account, patch = dict()):
    if (not patch):
        view_helper.verify_account_name (account)
        pre_check_function_call (command_name_enum.get_rm_state)
    
    query = [
        (controls.manage_user.get_groupname_from_username, {"username": account})
    ]
    
    result = execute_get_request_queries (query, {"Account" : account})
    
    view_helper.update_and_replace_status_information (result, patch)
    return view_helper.return_redfish_resource ("account", values = result)

@auth_basic (authentication.validate_user)
def get_roles ():
    return view_helper.return_redfish_resource ("roles")

@auth_basic (authentication.validate_user)
def get_ocs_admin ():
    return view_helper.return_redfish_resource ("admin")

@auth_basic (authentication.validate_user)
def get_ocs_operator ():
    return view_helper.return_redfish_resource ("operator")

@auth_basic (authentication.validate_user)
def get_ocs_user ():
    return view_helper.return_redfish_resource ("user")
