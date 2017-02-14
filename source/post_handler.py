import authentication
import view_helper
from bottle import HTTPError, auth_basic
from authentication import pre_check_function_call
from controls.utils import completion_code
from view_helper import parameter_parser
import controls.manage_user
import controls.manage_logentry
from authentication import pre_check_slot_id

def validate_action_parameters (validation):
    """
    Validate the parameters passed to the action.
    
    :param validation: The validation to perform on the parameters.  This is a mapping of parameter
    names to parser instances
    
    :return A dictionary containing the validated parameters.
    """
    
    data = view_helper.get_json_request_data ()
    params = {}
    errors = {}
    for param, parser in validation.items ():
        if (param in data):
            try:
                parser.parse_parameter (data[param], params)
            
            except Exception as error:
                view_helper.append_parameter_error (errors, view_helper.invalid_property_value_key,
                    str (error))
        else:
            view_helper.append_missing_parameter_error (errors, param)

    for param in data.keys ():
        if ((param not in validation) and ("@" not in param)):
            view_helper.append_unknown_parameter_error (errors, param)
    
    if errors:
        view_helper.raise_status_response (400, errors)
    
    return params

def check_action_result (result, success_code = 200, fail_code = 500):
    """
    Check the result of an action to see if it completed successfully.  If it did not, an exception
    is raised.
    
    :param result: The result of the action.
    :param success_code: The HTTP status code to return on success.
    :param fail_code: The HTTP status code to return on failure.
    
    :return A successful response message if no error occurred processing the action.
    """
    
    status = success_code if (result[completion_code.cc_key] == completion_code.success) else fail_code
    result = view_helper.create_response_with_status (code = result)
    return view_helper.return_status_response (status, result)
    



###################
# BMC components
###################
@auth_basic (authentication.validate_user)
def post_bmc_clear_log (slot_id):
    pre_check_slot_id(slot_id)
    result = controls.manage_logentry.clear_event_log()

    return check_action_result (result)

def post_bmc_fw_update(slot_id):
    pre_check_slot_id(slot_id)
    result ={}
    validation = {
        "Action" : parameter_parser ("action", str)
    }
    params = validate_action_parameters(validation)
    result = controls.manage_bmc.set_bmc_fwupdate(**params)
    return check_action_result(result)



def post_bmc_fw_update_state(slot_id):
    pre_check_slot_id(slot_id)
    result = {}
    validation = {
        "Action" : parameter_parser ("action", str)
    }
    params = validate_action_parameters(validation)
    result = controls.manage_bmc.get_bmc_fwupdate_state(**params)
    if result[completion_code.cc_key] == completion_code.failure:
        return check_action_result(result)
    return view_helper.return_redfish_resource ("bmc_fw_update_state", values = result)


def post_bmc_warm_reset(slot_id):
    pre_check_slot_id(slot_id)
    result ={}
    validation = {
        "Action" : parameter_parser ("action", str)
    }
    params = validate_action_parameters(validation)
    result = controls.manage_bmc.set_bmc_warm_reset(**params)
    return check_action_result(result)
#####################
# Chassis components
#####################

@auth_basic (authentication.validate_user)
def post_chassis_storage_enclosure_disk (slot_id, se_id, disk_id):
    pre_check_slot_id(slot_id)
    result = True
    return check_action_result (result)



############################
# Account service components
############################
@auth_basic (authentication.validate_user)
def post_accounts ():
    pre_check_function_call (command_name_enum.set_rm_config)
    
    validation = {
        "UserName" : parameter_parser ("username", str),
        "Password" : parameter_parser ("pwd", str),
        "RoleId" : parameter_parser ("role", str, RoleId)
    }
    params = validate_action_parameters (validation)
    
    result = controls.manage_user.user_create_new (**params)
    return check_action_result (result, success_code = 201)
