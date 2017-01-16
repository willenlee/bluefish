<%
    setdefault ("ID", "#")
%>

{

  "@Redfish.Copyright": "Copyright © 2014-2015 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",

  "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}",

  "@odata.context": "/redfish/v1/$metadata#Chassis.Chassis",

  "@odata.type": "#Chassis.v1_2_0.Chassis",

  "Id": "StorageEnclosure{{ID}}",

  "Name": "External Enclosure {{ID}}",

  "SKU": "Enclosure",

  "Manufacturer": "Manufacturer Name",

  "AssetTag": "External Enclosure",

  "Model": "External Enclosure",

  "ChassisType": "StorageEnclosure",

  "IndicatorLED": "Lit",

  "Status": {

    "State": "Enabled",

    "Health": "OK"

  },

  "Thermal": {

    "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Thermal"

  },

  "Power": {

    "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Power"

  },

  "Links": {

    "ManagedBy": [

      {

        "@odata.id": "/redfish/v1/Managers/1"

      }

    ],


    "Drives": [

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.0"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.1"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.2"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.3"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.4"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.5"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.6"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.7"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.8"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.9"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.10"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.11"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.12"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.13"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.14"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.15"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.16"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.17"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.18"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.19"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.20"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure{{ID}}/Drives/Disk.Bay.21"

      }

    ],

    "Oem": {}

  },

  "Oem": {}

}
