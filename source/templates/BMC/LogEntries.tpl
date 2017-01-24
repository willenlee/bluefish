{
    "@odata.type": "#LogEntryCollection.LogEntryCollection",
    "@odata.context": "/redfish/v1/$metadata#Managers/Members/1/LogServices/Members/Log/Entries/$entry",
    "@odata.id": "/redfish/v1/Managers/1/LogServices/Log/Entries",
    "Members@odata.count": {{len(members)}},
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
                    "@odata.id": "/redfish/v1/Managers/1/LogServices/Log/Entry/{{vs}}",
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
    ]
}
