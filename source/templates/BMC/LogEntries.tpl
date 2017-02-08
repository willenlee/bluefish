<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#LogEntryCollection",
  "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/LogServices/Log1/Entries",
  "@odata.type": "#LogEntryCollection.LogEntryCollection",
  "Name": "Log Service Collection",
  "Description": "Collection of Logs for this System",
  "members@odata.count": {{len(members)}},
  "members": [
        % for  i, (k, v) in enumerate(members.iteritems()):
        {
            <% if i != len(members)-1:
                    closetag = ","
                else:
                    closetag = ""
             end %>
            % for l, (ks, vs) in enumerate(v.iteritems()):
                <% if l != len(v)-1:
                        tag = ","
                    else:
                        tag = ""
                 end %>

                % if ks == "Id":
                    "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/LogServices/Log1/Entry/{{vs}}",
                    "@odata.type": "#LogEntry.1.0.2.LogEntry",
                    "Id": "{{vs}}",
                    "Name": "Log Entry {{vs}}"{{tag}}
                % elif ks == "ExpanderIndex":
                    "ExpanderIndex": "{{vs}}"{{tag}}
                % elif ks == "Severity":
                    "Severity": "{{vs}}"{{tag}}
                % elif ks == "Created":
                    "Created": "{{vs}}"{{tag}}
                % elif ks == "SensorType":
                    "SensorType": "{{vs}}"{{tag}}
                % elif ks == "SensorNumber":
                    "SensorNumber": "{{vs}}"{{tag}}
                % elif ks == "Message":
                    "Message": "{{vs}}"{{tag}}
                % end
            % end
        }{{closetag}}
        % end
    ],
      "Links": {
        "OriginOfCondition": {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal"
        },
        "Oem": {}
      },
      "Oem": {}
}

