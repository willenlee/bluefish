{
    "@odata.type": "#LogService.v1_0_2.LogService",
    "@odata.context": "/redfish/v1/$metadata#Managers/Members/1/LogServices/Members/$entity",
    "@odata.id": "/redfish/v1/Managers/1/LogServices/Log",
    "Id": "Log",
    "Name": "Rack Manager Log",
    "Status": {
        %if defined ("TelemetryDaemonStatus"):
             "State": "{{TelemetryDaemonStatus}}"
		%end
    },
    "Entries": {
        "@odata.id": "/redfish/v1/Managers/1/LogServices/Log/Entries"
    },
    "Actions": {
        "#LogService.ClearLog": {
            "target": "/redfish/v1/Managers/1/LogServices/Log/Actions/LogService.ClearLog"
        }
    }
}
