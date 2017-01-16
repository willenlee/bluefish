#!/usr/bin/env python

# Contributors Listed Below - COPYRIGHT 2016
# [+] International Business Machines Corp.
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

import sys
import logging
from rocket import Rocket
import bottle
import resources
import view_helper



class msocs_bottle (bottle.Bottle):
    def default_error_handler (self, res):
        bottle.response.content_type = "application/json"
        return view_helper.get_error_body (res.status_code, msg = res.body)
        
app = msocs_bottle (__name__)
resources.add_bottle_filters (app)
for resource in resources.REDFISH_RESOURCES.itervalues ():
    resource.register_resource (app, "common")


if __name__ == '__main__':

    log = logging.getLogger('Rocket.Errors')
    log.setLevel(logging.INFO)
    log.addHandler(logging.StreamHandler(sys.stdout))

    server = Rocket(
             ('0.0.0.0', 80),
        'wsgi', {'wsgi_app': app},
        min_threads=1,
        max_threads=1)
    server.start()
