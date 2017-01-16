{
    %if defined ("members"):
	    % for  i, (k, v) in enumerate(members.iteritems()):   
		     % if isinstance(v, dict):
			    % for l, (ks, vs) in enumerate(v.iteritems()): 
			    	   <% if l != len(v)-1:
				            tag = ","               
				        else: 
				            tag = ""
				        end %>
			           
			    	  % if ks == "RecordId":
							"@odata.id": "/redfish/v1/Managers/1/LogServices/Log/Entry/{{Entry}}",
							"@odata.type": "#LogEntry.v1_0_2.LogEntry",
							"@odata.context": "/redfish/v1/$metadata#Managers/Members/1/LogServices/Members/Log/Entries/Members/$entry",
			    	        "Id": "Entry{{Entry}}",
							"Name": "Log Entry {{Entry}}",
						    "MessageId": {{Entry}}{{tag}}	        
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
	 	% end 
 	% end       
}
