<%
    setdefault ("SLOT_ID", "#")
    setdefault ("PSU_ID", "#")
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
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerControl/0",
      "MemberId": "0",
      "Name": "Fan HSC Power",
      "PowerConsumedWatts": 8000,
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
        "HSC Status": "0x00",
        "HSC Status Manufacturer Specific": "0x00"
      }

    }
  ],
  "Voltages": [
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Voltages/0",
      "MemberId": "0",
      "Name": "P12V Voltage",
      "SensorNumber": 39,
      "Status": {
        "State": "Enabled",
        "Health": "OK"
      },
      "ReadingVolts": 12,
      "UpperThresholdCritical": 13.2,
      "LowerThresholdCritical": 10.8,
      "MinReadingRange": 0,
      "MaxReadingRange": 20,
      "PhysicalContext": "VoltageRegulator",
      "RelatedItem": [
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
      ]
    }
  ],
  "PowerSupplies": [
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/0",
      "MemberId": "0",
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
            "target":  "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/{{PSU_ID}}/Actions/PowerSupply.ClearFaults"
          },
          "#PowerSupply.FirmwareUpdate": {
            "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/ PowerSupplies/{{PSU_ID}}/Actions/PowerSupply.FirmwareUpdate",
              "FWRegion@Redfish.AllowableValues": [
                "A",
                "B",
                "Bootloader"
              ]
            },
          "#PowerSupply.FirmwareUpdateState": {
            "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/ PowerSupplies/{{PSU_ID}}/Actions/PowerSupply.FirmwareUpdateState",
            "Operation@Redfish.AllowableValues": [
              "Abort",
              "Query"
            ]
          }
        }
      },
      "PowerCapacityWatts": 1650,
      "LastPowerOutputWatts": 192,
      "Model": "499253-B21",
      "Manufacturer": "ManufacturerName",
      "FirmwareVersion": "1.00",
      "SerialNumber": "1z0000001",
      "PartNumber": "1z0000001A3a",

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
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/1",
      "MemberId": "0",
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
            "target":  "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/{{PSU_ID}}/Actions/PowerSupply.ClearFaults"
          },
          "#PowerSupply.FirmwareUpdate": {
            "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/ PowerSupplies/{{PSU_ID}}/Actions/PowerSupply.FirmwareUpdate",
              "FWRegion@Redfish.AllowableValues": [
                "A",
                "B",
                "Bootloader"
              ]
            },
          "#PowerSupply.FirmwareUpdateState": {
            "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/ PowerSupplies/{{PSU_ID}}/Actions/PowerSupply.FirmwareUpdateState",
            "Operation@Redfish.AllowableValues": [
              "Abort",
              "Query"
            ]
          }
        }
      },
      "PowerCapacityWatts": 1650,
      "LastPowerOutputWatts": 192,
      "Model": "499253-B21",
      "Manufacturer": "ManufacturerName",
      "FirmwareVersion": "1.00",
      "SerialNumber": "1z0000001",
      "PartNumber": "1z0000001A3a",

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
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/0",
      "MemberId": "0",
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