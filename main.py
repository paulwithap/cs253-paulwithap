#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

form="""
	<h1>Welcome</h1>
	<ul>
		<li><a href="/birthday">Birthday</a></li>
        <li><a href="/tagify">Tagify</a></li>
        <li><a href="/rot13">ROT 13</a></li>
	</ul>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	#self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(form)

    def post(self):
    	self.response.out.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
