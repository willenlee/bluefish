<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#Chassis",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/MainBoard",
  "@odata.type": "#Chassis.v1_3_0.Chassis",
  "Id": "MainBoard",
  "Name": "Management MainBoard",
  "ChassisType": "Module",
  "Manufacturer": "ManufacturerName",
  "Model": "ProductModelName",
  "SKU": "",
  "SerialNumber": "2M220100SL",
  "PartNumber": "",
  "AssetTag": "CustomerWritableThingy",
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
    "ManagedBy": [
      {
        "@odata.id": "1/redfish/v1/Managers/System/{{SLOT_ID}}"
      }
    ],
    "ManagersInChassis": [
      {
        "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}"
      }
    ],
    "Oem": {
      "RTCStatus": "OK",
      "FanControllerStatus": "OK"
    }
  }
}