<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",

"@odata.context": "/redfish/v1/$metadata#ChassisCollection",
  "@odata.id": "/redfish/v1/Chassis",
  "@odata.type": "#ChassisCollection.ChassisCollection",
  "Name": "Chassis Collection",
  "Members@odata.count": 6,
  "Members": [
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
    },
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/MainBoard"
    },
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure1"
    },
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure2"
    },
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure3"
    },
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure4"
    }
  ]
}