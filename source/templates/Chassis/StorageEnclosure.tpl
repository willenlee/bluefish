<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright © 2014-2015 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}",
  "@odata.context": "/redfish/v1/$metadata#Chassis",
  "@odata.type": "#Chassis.v1_3_0.Chassis",
  "Id": "StorageEnclosure{{SE_ID}}",
  "Name": "External Enclosure {{SE_ID}}",
  "SKU": "Enclosure",
  "Manufacturer": "{{manufacturer}}",
  "AssetTag": "External Enclosure",
  "Model": "External Enclosure",
  "ChassisType": "Module",
  "IndicatorLED": "{{id_led}}",
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  },
  "Storage": {
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Storage"
  },
  "Thermal": {
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Thermal"
  },
  "Power": {
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Power"
  },
  "Links": {
    "ManagedBy": [
      {
        "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}"
      }
    ],
    "Oem": {}
  },
  "Actions": {
    "Oem": {
      "Actions":{
        "#Chassis.MasterWriteRead": {
          "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Actions/Chassis.MasterWriteRead"
        },
        "#StorageEnclosure.PowerOn": {
          "Target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Actions/On"
        },
        "#StorageEnclosure.PowerOff": {
          "Target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Actions/Off"
        }
      }
    }
  },
  "Oem": {}
}
