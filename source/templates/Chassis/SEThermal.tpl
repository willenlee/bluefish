<%
    setdefault ("SE_ID", "#")
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright © 2014-2015 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosureSE_ID/Thermal",
  "@odata.context": "/redfish/v1/$metadata#Thermal",
  "@odata.type": "#Thermal.v1_1_0.Thermal",
  "Id": "Thermal",
  "Name": "Thermal",
  "Temperatures": [
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Thermal#/Temperatures/0",
      "MemberId": "0",
      "Name": "HDD Top Temp",
      "SensorNumber": 16,
      "Status": {
        "State": "Enabled",
        "Health": "OK"
      },
      "ReadingCelsius": 21,
      "UpperThresholdCritical": 42,
      "MinReadingRange": 0,
      "MaxReadingRange": 200,
      "PhysicalContext": "StorageBay",
      "RelatedItem": [
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}"
        }
      ]
    }
  ]
}