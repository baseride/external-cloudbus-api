# -*- coding: utf-8 -*-

# python 2.7 version

import json
import requests
import urlparse
from requests.auth import HTTPBasicAuth
import conf as apiconf
import baserideapiv2 as api2

try:

    api = api2.BaserideServletServletApi(apiconf.domain, apiconf.redirect_uri, apiconf.login, apiconf.password, apiconf.client_id, apiconf.client_secret)
    api.get_token()
    json_data = api.get_object_list()
    for obj in json_data['objects']:
        is_alive = obj['is_alive']
        is_started = obj['is_started']
        if not is_alive:
            print "Servlet", obj['name'], "is not alive"
        if not is_started:
            print "Servlet", obj['name'], "is not started"


except BaseException, ex:
    print 'ERR '+str(ex)
