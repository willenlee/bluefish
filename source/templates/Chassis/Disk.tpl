<%
    setdefault ("SE_ID", "#")
    setdefault ("DISK_ID", "#")
%>


{

  "@odata.context": "/redfish/v1/$metadata#Chassis/Members/Drives/Members/$entity",

  "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{SE_ID}}/Drives/Disk.{{DISK_ID}}",

  "@odata.type": "#Drive.v1_0_0.Drive",

  "IndicatorLED": "Lit",

  "Model": "ST9146802SS",

  "Revision": "S20A",

  "Status": {

    "State": "Enabled",

    "Health": "OK"

  },

  "CapacityBytes": 899527000000,

  "FailurePredicted": false,

  "Protocol": "SAS",

  "MediaType": "HDD",

  "Manufacturer": "SEAGATE",

  "SerialNumber": "72D0A037FRD26",

  "PartNumber": "SG0GP8811253178M02GJA00",

  "Identifiers": [

    {

      "DurableNameFormat": "NAA",

      "DurableName": "500003942810D13B"

    }

  ],

  "AssetTag": "",

  "CapableSpeedGbs": 12,

  "NegotiatedSpeedGbs": 12,

  "Links": {

  },

  "Actions": {

    "#Drive.On": {

      "Target": "/redfish/v1/Chassis/StorageEnclosure{{SE_ID}}/Drives/Disk.Bay.{{DISK_ID}}/Actions/On"

    },

    "#Drive.Off": {

      "Target": "/redfish/v1/Chassis/StorageEnclosure1{{SE_ID}}/Drives/Disk.BAy.{{DISK_ID}}/Actions/Off"

    }

  }

}
