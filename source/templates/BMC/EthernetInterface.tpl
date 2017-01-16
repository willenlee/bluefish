<%
    if defined ("TemplateDefault"):
        setdefault ("Intf", "")
        setdefault ("Description", "")
        setdefault ("InterfaceHealth", "")
        setdefault ("InterfaceStatus", "")
        setdefault ("MacAddress", "")
        setdefault ("IPAddress", "")
        setdefault ("SubnetMask", "")
        setdefault ("Origin", "")
        setdefault ("Gateway", "")
    end
%>
{
    "@odata.type": "#EthernetInterface.v1_0_0.EthernetInterface",
    "@odata.context": "/redfish/v1/$metadata#Managers/Members/RackManager/EthernetInterfaces/Members/$entity",
    "@odata.id": "/redfish/v1/Managers/RackManager/EthernetInterface/{{Intf}}",
    "Id": "{{Intf}}",
    "Name": "{{Intf}}",
    "Description": "{{Description}}",
    "Status": {
    	<% if defined ("InterfaceHealth"):
    		tag = ","
		else:
			tag = ""
		end %>
    
        % if defined ("InterfaceStatus"):        	
        	"State": "{{InterfaceStatus}}"{{tag}}
		% end
        % if defined ("InterfaceHealth"):    
        	"Health": "{{InterfaceHealth}}"
        % end
    },
    % if defined ("MacAddress"):    
    	"PermanentMACAddress": "{{MacAddress}}",
	% end
    "IPv4Addresses": [
        {
	        % if defined ("IPAddress"):    
		    	"Address": "{{IPAddress}}",
			% end
			% if defined ("SubnetMask"):    
		    	"SubnetMask": "{{SubnetMask}}",
			% end
			% if defined ("Origin"):    
		    	"AddressOrigin": "{{Origin}}",
			% end
			% if defined ("Gateway"):    
		    	"Gateway": "{{Gateway}}"
			% end
        }
    ]
}
