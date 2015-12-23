# -*- coding: utf-8 -*-

# python 2.7 version

import json
import requests
import urlparse
from requests.auth import HTTPBasicAuth

requests.packages.urllib3.disable_warnings()

try:

    # change it:
    login = 'login'
    password = 'password'
    client_id = 'your application client id'
    client_secret = 'your application client secret key'

    ###

    # registration in Cloudbus:
    resp = requests.get('https://baseride.com/oauth2/authorize/?response_type=code&client_id='+client_id, auth=HTTPBasicAuth(login,password), allow_redirects=False)
    if resp.status_code!=302 or not resp.headers['Location'] or not resp.headers['Location'].startswith('http://baseride.com/?code='):
        print 'ERR code '+str(resp.status_code)
        quit()

    code = urlparse.urlparse(resp.headers['Location']).query.split('=')[1]
    resp = requests.get('https://baseride.com/oauth2/token/?callback=call_back&client_id='+client_id+'&client_secret='+client_secret+'&code=' +code+ '&grant_type=authorization_code&redirect_uri=http://baseride.com/', allow_redirects=False)
    if resp.status_code!=200:
        print 'ERR code '+str(resp.status_code)
        quit()

    json_str = str(resp.content).split('call_back(')[1].split(');')[0]
    json_data = json.loads(json_str)
    token = json_data[u'access_token']

    # applied api calls :

    # user profile
    resp = requests.get('https://baseride.com/api/v2/profile/whoami/?format=json', headers={'Authorization': 'BEARER '+token})
    if resp.status_code!=200:
        print 'ERR code '+str(resp.status_code)
        quit()
    json_data = json.loads(resp.text)
    # ...

    # vehicle info
    vehicle_id = 29687 # vehicle from Demo Cloudbus; change it to correct vehicle id
    url = 'https://baseride.com/api/v2/transport/vehicle/'+str(vehicle_id)+'/?format=json'
    resp = requests.get(url, headers={'Authorization': 'BEARER '+token})
    if resp.status_code!=200:
        print 'ERR code '+str(resp.status_code)
        quit()
    json_data = json.loads(resp.text)
    # ...

except BaseException, ex:
    print 'ERR '+str(ex)
