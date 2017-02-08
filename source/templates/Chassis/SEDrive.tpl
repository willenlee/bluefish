<%
    setdefault ("SE_ID", "#")
    setdefault ("SLOT_ID", "#")
    setdefault ("DRIVE_ID", "#")
%>

{
  "@odata.context": "/redfish/v1/$metadata#Drive",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Drives/Drive{{DRIVE_ID}}",
  "@odata.type": "#Drive.v1_1_0.Drive",
  "IndicatorLED": "Lit",
  "Revision": "S20A",
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  },
  "MediaType": "HDD",
  "CapableSpeedGbs": 12,
  "NegotiatedSpeedGbs": 12,
  "Links": {
  },
  "Actions": {
    "#Drive.On": {
      "Target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Drives/Drive{{DRIVE_ID}}/Actions/On"
    },
    "#Drive.Off": {
      "Target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Drives/Drive{{DRIVE_ID}}/Actions/Off"
    }
  }
}