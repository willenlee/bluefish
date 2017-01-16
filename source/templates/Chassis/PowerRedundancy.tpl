{

  "@odata.id": "/redfish/v1/Chassis/1/Power#/Redundancy/0",

  "MemberId": "0",

  "Name": "PowerSupply Redundancy Group 1",

  "Mode": "Failover",

  "MaxNumSupported": 2,

  "MinNumNeeded": 1,

  "RedundancySet": [

    {

      "@odata.id": "/redfish/v1/Chassis/1/Power#/PowerSupplies/0"

    },

    {

      "@odata.id": "/redfish/v1/Chassis/1/Power#/PowerSupplies/1"

    }

  ],

  "Status": {

    "State": "Offline",

    "Health": "OK"

  }

}
