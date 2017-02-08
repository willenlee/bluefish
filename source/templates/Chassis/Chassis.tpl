<%
    setdefault ("SLOT_ID", "#")
    if defined ("TemplateDefault"):
        setdefault ("Chassis_IndicatorLED", "")
    end
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#Chassis",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}",
  "@odata.type": "#Chassis.v1_3_0.Chassis",
  "Id": "1",
  "Name": "Computer System Chassis",
  "ChassisType": "RackMount",
  "Manufacturer": "ManufacturerName",
  "Model": "ProductModelName",
  "SKU": "",
  "SerialNumber": "2M220100SL",
  "PartNumber": "",
  "AssetTag": "CustomerWritableThingy",
  % if defined ("Chassis_IndicatorLED"):
  "IndicatorLED": "{{Chassis_IndicatorLED}}",
  % end
  "PowerState": "On",
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