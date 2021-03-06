# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2017 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import json
from http.server import BaseHTTPRequestHandler
from urllib import parse


class FakeSnapdServer(BaseHTTPRequestHandler):

    snaps_not_found = []
    installed_snaps = []

    def do_GET(self):
        parsed_url = parse.urlparse(self.path)
        if parsed_url.path.startswith('/v2/snaps/'):
            self._handle_snaps(parsed_url)
        elif parsed_url.path == '/v2/find':
            self._handle_find(parsed_url)
        else:
            self.wfile.write(parsed_url.path.encode())

    def _handle_snaps(self, parsed_url):
        status_code = 404
        params = {}

        if parsed_url.path.endswith('/fake-snap'):
            status_code = 200
            params = {
                'channel': 'stable',
                'revision': 'test-fake-snap-revision'
            }
        elif parsed_url.path.endswith('/fake-snap-stable'):
            status_code = 200
            params = {'channel': 'stable'}
        elif parsed_url.path.endswith('/fake-snap-branch'):
            status_code = 200
            params = {'channel': 'candidate/branch'}
        elif parsed_url.path.endswith('/fake-snap-track-stable'):
            status_code = 200
            params = {'channel': 'track/stable'}
        elif parsed_url.path.endswith('/fake-snap-track-stable-branch'):
            status_code = 200
            params = {'channel': 'track/stable/branch'}
        elif parsed_url.path.endswith('/fake-snap-edge'):
            status_code = 200
            params = {'channel': 'edge'}
        elif (parsed_url.path in self.snaps_not_found and
              parsed_url.path.split('/')[-1] in self.installed_snaps):
            # XXX when the snaps end point fails, the snap is installed and
            # it needs a revision the next time the same endpoint is called.
            status_code = 200
            params = {'channel': 'dummy', 'revision': 'dummy'}
        else:
            self.snaps_not_found.append(parsed_url.path)

        self.send_response(status_code)
        self.send_header('Content-Type', 'text/application+json')
        self.end_headers()
        response = json.dumps({'result': params}).encode()
        self.wfile.write(response)

    def _handle_find(self, parsed_url):
        query = parse.parse_qs(parsed_url.query)
        status_code = 404
        params = {}

        if query['name'][0] == 'fake-snap':
            status_code = 200
            params = {'channels': {
                'latest/stable': {'confinement': 'strict'},
                'classic/stable': {'confinement': 'classic'},
                'strict/stable': {'confinement': 'strict'},
                'devmode/stable': {'confinement': 'devmode'},
            }}
        if query['name'][0] == 'new-fake-snap':
            status_code = 200
            params = {'channels': {
                'latest/stable': {'confinement': 'strict'},
            }}

        self.send_response(status_code)
        self.send_header('Content-Type', 'text/application+json')
        self.end_headers()
        response = json.dumps({'result': [params]}).encode()
        self.wfile.write(response)
