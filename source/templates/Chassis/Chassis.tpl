<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#Chassis",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}",
  "@odata.type": "#Chassis.v1_3_0.Chassis",
  "Id": "{{SLOT_ID}}",
  "Name": "Computer System Chassis",
  "ChassisType": "RackMount",
  "Manufacturer": "{{manufacturer}}",
  "Model": "{{model_name}}",
  "SKU": "",
  "SerialNumber": "{{serial_number}}",
  "PartNumber": "{{part_number}}",
  "AssetTag": "{{asset_tag}}",
  "IndicatorLED": "{{Chassis_IndicatorLED}}",
  "PowerState": "{{power_state}}",
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  },
  "Thermal": {
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal"
  },
  "Power": {
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power"
  },
  "Links": {
    "Contains": [
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/MainBoard"
      },
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure1"
      },
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure1"
      },
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure3"
      },
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure4"
      }
    ],
    "ManagedBy": [
      {
        "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}"
      }
    ],
    "Oem": {}
  },
  "Oem": {}
}