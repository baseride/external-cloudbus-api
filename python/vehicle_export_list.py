# -*- coding: utf-8 -*-

# python 2.7 version

import json
import requests
import urlparse
from requests.auth import HTTPBasicAuth
import conf as apiconf
import baserideapiv2 as api2

try:
    api = api2.BaserideVehicleApi(apiconf.domain, apiconf.redirect_uri, apiconf.login, apiconf.password, apiconf.client_id, apiconf.client_secret)
    api.get_token()
    offset = 0
    limit = 1000
    next_url = 1
    f = open('vehicles.csv', 'w+')
    f.write("#,Registration code,Enterprise\n")
    i = 0
    while offset < 3000:
        print "offset", offset
        json_data = api.get_object_list(offset,limit)
        for obj in json_data['objects']:
            if obj['kind'] != 'mobile':
                i += 1
                f.write("{},{},{}\n".format(i,obj['registration_code'],obj['park_info']['enterprise_info']['name']) )
        offset = offset + limit
        next_url = json_data['meta']['next']
    f.close()

except BaseException, ex:
    print 'ERR '+str(ex)
