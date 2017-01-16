{

  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",

  "@odata.context": "/redfish/v1/$metadata#Chassis.Chassis",

  "@odata.id": "/redfish/v1/Chassis/Enc1",

  "@odata.type": "#Chassis.v1_0_0.Chassis",

  "Id": "Enc1",

  "Name": "Enclosure 1",

  "Description": "Enclosure with storage expanders.  It also is managed by a manager.",

  "ChassisType": "Enclosure",

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


  "Links": {

    },

    "ManagedBy": [

      {

        "@odata.id": "1/redfish/v1/Managers/1"

      },

    ],

    "Contains": [

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure1"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure2"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure3"

      },

      {

        "@odata.id": "/redfish/v1/Chassis/StorageEnclosure4"

      }

    ],

    "Oem": {}

  }

}
