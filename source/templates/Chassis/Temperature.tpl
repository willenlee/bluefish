{

  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",

  "@odata.context": "/redfish/v1/$metadata#Thermal.Thermal",

  "@odata.id": "/redfish/v1/Chassis/1/Thermal",

  "@odata.type": "#Thermal.v1_1_0.Thermal",

  "Id": "Thermal",

  "Name": "Thermal",

  "Temperatures": [

    {

      "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Temperatures/0",

      "MemberId": "0",

      "Name": "Ambient Temp 1",

      "SensorNumber": 42,

      "Status": {

        "State": "Enabled",

        "Health": "OK"

      },

      "ReadingCelsius": 21,

      "UpperThresholdNonCritical": 42,

      "UpperThresholdCritical": 42,

      "UpperThresholdFatal": 42,

      "LowerThresholdNonCritical": 42,

      "LowerThresholdCritical": 5,

      "LowerThresholdFatal": 42,

      "MinReadingRange": 0,

      "MaxReadingRange": 200,

      "PhysicalContext": "Sensor"

    },

    {

      "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Temperatures/1",

      "MemberId": "1",

      "Name": "Ambient Temp 2",

      "SensorNumber": 43,

      "Status": {

        "State": "Enabled",

        "Health": "OK"

      },

      "ReadingCelsius": 21,

      "UpperThresholdNonCritical": 42,

      "UpperThresholdCritical": 42,

      "UpperThresholdFatal": 42,

      "LowerThresholdNonCritical": 42,

      "LowerThresholdCritical": 5,

      "LowerThresholdFatal": 42,

      "MinReadingRange": 0,

      "MaxReadingRange": 200,

      "PhysicalContext": "Sensor"

    },

    {

      "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Temperatures/2",

      "MemberId": "2",

      "Name": "Chassis Intake Temp",

      "SensorNumber": 44,

      "Status": {

        "State": "Enabled",

        "Health": "OK"

      },

      "ReadingCelsius": 25,

      "UpperThresholdNonCritical": 30,

      "UpperThresholdCritical": 40,

      "UpperThresholdFatal": 50,

      "LowerThresholdNonCritical": 10,

      "LowerThresholdCritical": 5,

      "LowerThresholdFatal": 0,

      "MinReadingRange": 0,

      "MaxReadingRange": 200,

      "PhysicalContext": "Intake",

      "RelatedItem": [

        {

          "@odata.id": "/redfish/v1/Chassis/1"

        }

      ]

    }

  ],

  "Fans": [

    {

      "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Fans/0",

      "MemberId": "0",

      "Name": "BaseBoard System Fan",

      "PhysicalContext": "Backplane",

      "Status": {

        "State": "Enabled",

        "Health": "OK"

      },

      "Reading": 2100,

      "ReadingUnits": "RPM",

      "UpperThresholdNonCritical": 42,

      "UpperThresholdCritical": 4200,

      "UpperThresholdFatal": 42,

      "LowerThresholdNonCritical": 42,

      "LowerThresholdCritical": 5,

      "LowerThresholdFatal": 42,

      "MinReadingRange": 0,

      "MaxReadingRange": 5000,

      "Redundancy": [

        {

          "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Redundancy/0"

        }

      ],

      "RelatedItem": [

        {

          "@odata.id": "/redfish/v1/Chassis/1"

        }

      ]

    },

    {

      "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Fans/1",

      "MemberId": "1",

      "Name": "BaseBoard System Fan Backup",

      "PhysicalContext": "Backplane",

      "Status": {

        "State": "Enabled",

        "Health": "OK"

      },

      "Reading": 2100,

      "ReadingUnits": "RPM",

      "UpperThresholdNonCritical": 42,

      "UpperThresholdCritical": 4200,

      "UpperThresholdFatal": 42,

      "LowerThresholdNonCritical": 42,

      "LowerThresholdCritical": 5,

      "LowerThresholdFatal": 42,

      "MinReadingRange": 0,

      "MaxReadingRange": 5000,

      "Redundancy": [

        {

          "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Redundancy/0"

        }

      ],

      "RelatedItem": [

        {

          "@odata.id": "/redfish/v1/Chassis/1"

        }

      ]

    },
    {

      "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Fans/2",

      "MemberId": "2",

      "Name": "BaseBoard System Fan Backup",

      "PhysicalContext": "Backplane",

      "Status": {

        "State": "Enabled",

        "Health": "OK"

      },

      "Reading": 2100,

      "ReadingUnits": "RPM",

      "UpperThresholdNonCritical": 42,

      "UpperThresholdCritical": 4200,

      "UpperThresholdFatal": 42,

      "LowerThresholdNonCritical": 42,

      "LowerThresholdCritical": 5,

      "LowerThresholdFatal": 42,

      "MinReadingRange": 0,

      "MaxReadingRange": 5000,

      "Redundancy": [

        {

          "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Redundancy/0"

        }

      ],

      "RelatedItem": [

        {

          "@odata.id": "/redfish/v1/Chassis/1"

        }

      ]

    },
    {

      "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Fans/3",

      "MemberId": "3",

      "Name": "BaseBoard System Fan Backup",

      "PhysicalContext": "Backplane",

      "Status": {

        "State": "Enabled",

        "Health": "OK"

      },

      "Reading": 2100,

      "ReadingUnits": "RPM",

      "UpperThresholdNonCritical": 42,

      "UpperThresholdCritical": 4200,

      "UpperThresholdFatal": 42,

      "LowerThresholdNonCritical": 42,

      "LowerThresholdCritical": 5,

      "LowerThresholdFatal": 42,

      "MinReadingRange": 0,

      "MaxReadingRange": 5000,

      "Redundancy": [

        {

          "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Redundancy/0"

        }

      ],

      "RelatedItem": [

        {

          "@odata.id": "/redfish/v1/Chassis/1"

        }

      ]

    }

  ],

  "Redundancy": [

    {

      "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Redundancy/0",

      "MemberId": "0",

      "Name": "BaseBoard System Fans",

      "RedundancyEnabled": false,

      "RedundancySet": [

        {

          "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Fans/0"

        },

        {

          "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Fans/1"

        },

        {

          "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Fans/2"

        },

        {

          "@odata.id": "/redfish/v1/Chassis/1/Thermal#/Fans/3"

        }

      ],

      "Mode": "N+m",

      "Status": {

        "State": "Disabled",

        "Health": "OK"

      },

      "MinNumNeeded": 3,

      "MaxNumSupported": 4

    }

  ]

}
