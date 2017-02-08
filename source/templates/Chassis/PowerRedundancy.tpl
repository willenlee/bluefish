<%
    setdefault ("SLOT_ID", "#")
%>

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