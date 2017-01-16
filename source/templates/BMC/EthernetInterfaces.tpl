{
    "@odata.type": "#EthernetInterfaceCollection.EthernetInterfaceCollection",
    "@odata.context": "/redfish/v1/$metadata#Managers/Members/1/EthernetInterfaces/$entity",
    "@odata.id": "/redfish/v1/Managers/1/EthernetInterfaces",
    "Name": "Ethernet Interface Collection",
	"Description": "Rack Manager Ethernet Interfaces",
    %if defined ("Interfaces_list"):
	    "Members@odata.count": {{len(Interfaces_list)}},
	    "Members": [
	    	% for  i, (k, v) in enumerate(Interfaces_list.iteritems()):   
	    	{      
			    <% if i != len(Interfaces_list)-1:
			            closetag = ","               
			       else: 
			            closetag = ""
			     end %>
			     "@odata.id": "/redfish/v1/Managers/1/EthernetInterface/{{v}}"
		    }{{closetag}}
	 	    % end
	    ]
    %end
}
