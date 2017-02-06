{

  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",

  "@odata.context": "/redfish/v1/$metadata#ManagerNetworkProtocol.ManagerNetworkProtocol",

  "@odata.id": "/redfish/v1/Managers/1/NetworkProtocol",

  "@odata.type": "#ManagerNetworkProtocol.v1_0_0.ManagerNetworkProtocol",

  "Id": "NetworkProtocol",

  "Name": "Manager Network Protocol",

  "Description": "Manager Network Service Status",

  "Status": {

    "State": "Enabled",

    "Health": "OK"

  },

  "HostName": "StorageMgr",

  "FQDN": "none ",

  "HTTP": {

    "ProtocolEnabled": true,

    "Port": 80

  },

  "HTTPS": {

    "ProtocolEnabled": true,

    "Port": 443

  },

  "SSH": {

    "ProtocolEnabled": true,

    "Port": 22

  },

  "Telnet": {

    "ProtocolEnabled": false,

    "Port": 23

  },


  "Oem": {}

}
