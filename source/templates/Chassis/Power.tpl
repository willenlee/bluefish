<%
    setdefault ("SLOT_ID", "#")

    setdefault ("fan_HSC_Power_sensor_name", "")
    setdefault ("power_consumed_watts", "")
    setdefault ("HSC_status", "")
    setdefault ("HSC_status_MFR", "")

    setdefault ("reading_value", "")
    setdefault ("upper_critical_threshold", "")
    setdefault ("lower_critical_threshold", "")

    setdefault ("psu1_power_capacity", "")
    setdefault ("psu1_power_output_watt", "")
    setdefault ("psu1_model_number", "")
    setdefault ("psu1_manufacturer_name", "")
    setdefault ("psu1_firmware_version", "")    
    setdefault ("psu1_serial_number", "")
    setdefault ("psu1_part_number", "")

    setdefault ("psu2_power_capacity", "")
    setdefault ("psu2_power_output_watt", "")
    setdefault ("psu2_model_number", "")
    setdefault ("psu2_manufacturer_name", "")
    setdefault ("psu2_firmware_version", "")    
    setdefault ("psu2_serial_number", "")
    setdefault ("psu2_part_number", "")
%>

{
    "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
    "@odata.context": "/redfish/v1/$metadata#Power",
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power",
    "@odata.type": "#Power.v1_2_0.Power",
    "Id": "Power",
    "Name": "Power",
    "PowerControl": [
    {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerControl/1",
        "MemberId": "1",
        "Name": "{{fan_HSC_Power_sensor_name}}",
        "PowerConsumedWatts": "{{power_consumed_watts}}",
        "PowerLimit": {
            "LimitInWatts": 9000,
            "LimitException": "LogEventOnly"
        },
        "RelatedItem": [
        {
            "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
        ],
        "Status": {
            "State": "Enabled",
            "Health": "OK"
        },
        "Oem": {
            "HSC Status": "{{HSC_status}}",
            "HSC Status Manufacturer Specific": "{{HSC_status_MFR}}"
        }
    }
    ],
    "Voltages": [
    % for  i, (k, v) in enumerate(Voltages.iteritems()):
    {
        <% if i != len(Voltages)-1:
                closetag = ","
            else:
                closetag = ""
        end %>
        % for l, (ks, vs) in enumerate(v.iteritems()):
            % if ks == "sensor_id":
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Voltages/{{vs}}",
                "MemberId": "{{vs}}",
            % elif ks == "sensor_number":
                "SensorNumber": "{{vs}}",
            % elif ks == "sensor_name":
                "Name": "{{vs}}",
            % elif ks == "reading_value":
                "ReadingVolts": "{{vs}}",
            % elif ks == "upper_critical_threshold":
                "UpperThresholdCritical": "{{vs}}",
            % elif ks == "lower_critical_threshold":
                "LowerThresholdCritical": "{{vs}}",
            % end
        % end
        "Status": {
            "State": "Enabled",
            "Health": "OK"
        },
        "RelatedItem": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
            }
        ]
    }{{closetag}}
    % end
    ],
    "PowerSupplies": [
    {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/1",
        "MemberId": "1",
        "Name": "Power Supply Bay 1",
        "Status": {
            "State": "Enabled",
            "Health": "Warning",
            "Oem": {
                "Microsoft": {
                    "@odata.type": "#OcsPower.v1_0_0.Status",
                    "Faults": "Faults"
                }
            }
        },
        "Oem": {
            "Actions": {
                "#PowerSupply.ClearFaults": {
                    "target":  "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/1/Actions/PowerSupply.ClearFaults"
                },
                "#PowerSupply.FirmwareUpdate": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/1/Actions/PowerSupply.FirmwareUpdate",
                    "FWRegion@Redfish.AllowableValues": [
                        "A",
                        "B",
                        "Bootloader"
                    ]
                },
                "#PowerSupply.FirmwareUpdateState": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/1/Actions/PowerSupply.FirmwareUpdateState",
                    "Operation@Redfish.AllowableValues": [
                        "Abort",
                        "Query"
                    ]
                }
            }
        },
        "PowerCapacityWatts": "{{psu1_power_capacity}}",
        "LastPowerOutputWatts": "{{psu1_power_output_watt}}",
        "Model": "{{psu1_model_number}}",
        "Manufacturer": "{{psu1_manufacturer_name}}",
        "FirmwareVersion": "{{psu1_firmware_version}}",
        "SerialNumber": "{{psu1_serial_number}}",
        "PartNumber": "{{psu1_part_number}}",
        "RelatedItem": [
        {
            "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
        ],
        "Redundancy": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/0"
            }
        ]
    },
    {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/2",
        "MemberId": "2",
        "Name": "Power Supply Bay 2",
        "Status": {
            "State": "Enabled",
            "Health": "Warning",
            "Oem": {
                "Microsoft": {
                    "@odata.type": "#OcsPower.v1_0_0.Status",
                    "Faults": "Faults"
                }
            }
        },
        "Oem": {
            "Actions": {
                "#PowerSupply.ClearFaults": {
                    "target":  "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/2/Actions/PowerSupply.ClearFaults"
                },
                "#PowerSupply.FirmwareUpdate": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/2/Actions/PowerSupply.FirmwareUpdate",
                    "FWRegion@Redfish.AllowableValues": [
                        "A",
                        "B",
                        "Bootloader"
                    ]
                },
                "#PowerSupply.FirmwareUpdateState": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/2/Actions/PowerSupply.FirmwareUpdateState",
                    "Operation@Redfish.AllowableValues": [
                        "Abort",
                        "Query"
                    ]
                }
            }
        },
        "PowerCapacityWatts": "{{psu2_power_capacity}}",
        "LastPowerOutputWatts": "{{psu2_power_output_watt}}",
        "Model": "{{psu2_model_number}}",
        "Manufacturer": "{{psu2_manufacturer_name}}",
        "FirmwareVersion": "{{psu2_firmware_version}}",
        "SerialNumber": "{{psu2_serial_number}}",
        "PartNumber": "{{psu2_part_number}}",
        "RelatedItem": [
        {
            "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
        ],
        "Redundancy": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/0"
            }
        ]
    }
    ],
    "Redundancy": [
    {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/1",
        "MemberId": "1",
        "Name": "PowerSupply Redundancy Group 1",
        "Mode": "Failover",
        "MaxNumSupported": 2,
        "MinNumNeeded": 1,
        "RedundancySet": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/0"
            },
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/1"
            }
        ],
        "Status": {
            "State": "Offline",
            "Health": "OK"
        }
    }
    ],
    "Oem": {}
}