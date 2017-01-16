{
    "@odata.type": "#LogEntryCollection.LogEntryCollection",
    "@odata.context": "/redfish/v1/$metadata#Managers/Members/1/LogServices/Members/Log/Entries/$entry",
    "@odata.id": "/redfish/v1/Managers/1/LogServices/Log/Entries",
	"Name": "Log Entry Collection",
    % if defined ("members"):
	    "Members@odata.count": {{len(members)}},
	    "Members": [
	    	% for  i, (k, v) in enumerate(members.iteritems()):   
	    	{      
			    <% if i != len(members)-1:
			            closetag = ","               
			       else: 
			            closetag = ""
			     end %>
			     % if isinstance(v, dict):
				    % for l, (ks, vs) in enumerate(v.iteritems()): 
				    	   <% if l != len(v)-1:
					            tag = ","               
					        else: 
					            tag = ""
					        end %>
				           
				    	  % if ks == "RecordId":
				    		    "@odata.id": "/redfish/v1/Managers/1/LogServices/Log/Entry/{{vs}}",
				    		    "@odata.type": "#LogEntry.1.0.2.LogEntry",	
				    	        "Id": "Entry{{vs}}",
	            		        "Name": "Log Entry {{vs}}",
			                    "MessageId": "{{vs}}"{{tag}}	        
	        			  % elif ks == "SensorType":
	        			        "SensorType": "{{vs}}"{{tag}}
	        			  % elif ks == "Severity":
	        			        "Severity": "{{vs}}"{{tag}}
	        			  % elif ks == "Created":
	        			        "Created": "{{vs}}"{{tag}}
	        			  % elif ks == "Message":
	        			        "Message": "{{vs}}"{{tag}}
				          % elif ks == "Oem":
				          		 "Oem": {
					                "Microsoft": {
					                    "@odata.type": "#Ocs.v1_0_0.LogEntry",
					                    % if isinstance(vs, dict):
										    % for j, (koem, voem) in enumerate(vs.iteritems()):
										    	  <% if j != len(vs)-1:
											            eol = ","               
											       else: 
											            eol = ""
											      end %>
										            
										    	  % if koem == "Component":
									                    "Component": "{{voem}}"{{eol}}	        
							        			  % elif koem == "PortId":
							        			        "PortId": "{{voem}}"{{eol}}
						        			      % elif koem == "DeviceId":
							        			        "DeviceId": "{{voem}}"{{eol}}		
					        			          % elif koem == "FanId":
							        			        "FanId": "{{voem}}"{{eol}}			        			      		
						        			      % end
				        			      	% end
			        			      	% end
					                }
					             }{{tag}}
				    	  % end
		    		% end
		        % end
	    	}{{closetag}}
		 	% end
	    ]
    %end
}
