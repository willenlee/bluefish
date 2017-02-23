#!/usr/bin/python
# -*- coding: utf-8 -*-



from utils import *
import sys
sys.path.append('/usr/sbin')
import exp_lib
exp =  exp_lib.expander()

DEFAULT_OUTDATA_SIZE = 256

def se_i2c_master_write_read(se_id, writedata):
    result = {}
    if ("0x" in writedata) != True:
        return set_failure_dict("Hexadecimal numbers must prefixed with 0x?", completion_code.failure)
    exp_id = int(se_id) - 1
    write_data = str(writedata.replace('0x', ''))
    try:
        rdata = exp.handle_request(int(exp_id), write_data, DEFAULT_OUTDATA_SIZE)

    except Exception, e:
        return set_failure_dict("Master Write Read failed", completion_code.failure)
    result["BytesRead"] = str(rdata)
    result[completion_code.cc_key] = completion_code.success
    return result
