<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#Thermal",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal",
  "@odata.type": "#Thermal.v1_1_0.Thermal",
  "Id": "Thermal",
  "Name": "Thermal",
  "Temperatures": [
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Temperatures/0",
      "MemberId": "0",
      "Name": "Main Board Temp",
      "SensorNumber": 16,
      "Status": {
        "State": "Enabled",
        "Health": "OK"
      },
      "ReadingCelsius": 21,
      "UpperThresholdCritical": 42,
      "MinReadingRange": 0,
      "MaxReadingRange": 200,
      "PhysicalContext": "SystemBoard",
      "RelatedItem": [
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
      ]
    }

  ],
  "Fans": [
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/0",
      "MemberId": "0",
      "Name": "BaseBoard System Fan",
      "PhysicalContext": "Backplane",
      "Status": {
        "State": "Enabled",
        "Health": "OK"
      },
      "Reading": 2100,
      "ReadingUnits": "RPM",
      "UpperThresholdCritical": 4200,
      "LowerThresholdCritical": 5,
      "MinReadingRange": 0,
      "MaxReadingRange": 5000,
      "Oem": {
        "PWM": 50
      },
      "Redundancy": [
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Redundancy/0"
        }
      ],
      "RelatedItem": [
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
      ]
    }
  ],
  "Redundancy": [
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Redundancy/0",
      "MemberId": "0",
      "Name": "BaseBoard System Fans",
      "RedundancyEnabled": false,
      "RedundancySet": [
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/0"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/1"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/2"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/3"
        }
      ],
      "Mode": "N+m",
      "Status": {
        "State": "Disabled",
        "Health": "OK"
      },
      "MinNumNeeded": 3,
      "MaxNumSupported": 4
    }
  ]
}