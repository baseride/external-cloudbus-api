# -*- coding: utf-8 -*-

# python 2.7 version

import json
import requests
import urlparse
from requests.auth import HTTPBasicAuth

requests.packages.urllib3.disable_warnings()

class BaserideApi:
    
    def __init__(self, domain, redirect_uri, login, password, client_id, client_secret):
        self.auth_url = 'oauth2/authorize/?response_type=code&client_id='
        self.oath2token_url = 'oauth2/token/?callback=call_back&client_id='        
        self.domain = domain
        self.redirect_uri = redirect_uri
        self.login = login
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.set_base_url()

    def get_base_url(self):
        return self.base_url

    def set_base_url(self):
        self.base_url = ""
    
    def get_token(self):

        # registration in Cloudbus:
        resp = requests.get(self.domain + self.auth_url + self.client_id, auth=HTTPBasicAuth(self.login,self.password), allow_redirects=False)
        if resp.status_code!=302 or not resp.headers['Location'] or not resp.headers['Location'].startswith(self.redirect_uri+'?code='):
            print 'LINE A. ERR code '+str(resp.status_code)
            self.access_token = None
            return None

        code = urlparse.urlparse(resp.headers['Location']).query.split('=')[1]
        resp = requests.get(self.domain + self.oath2token_url + self.client_id + '&client_secret='+self.client_secret+'&code=' +code+ '&grant_type=authorization_code&redirect_uri=' + self.redirect_uri, allow_redirects=False)
        if resp.status_code!=200:
            print 'LINE B. ERR code '+str(resp.status_code)
            self.access_token = None
            return None

        json_str = str(resp.content).split('call_back(')[1].split(');')[0]
        json_data = json.loads(json_str)
        self.access_token = json_data[u'access_token']
        return self.access_token

    def get_object_list_url(self,offset=0,limit=20):
        url = self.domain + self.base_url + '?format=json&access_token=' + self.access_token + '&offset=' + str(offset) + '&limit=' + str(limit)
        return url

    def get_object_list(self,offset=0,limit=20):
        url = self.get_object_list_url(offset, limit)
        print "getting object list", url
        resp = requests.get( url )

        if resp.status_code!=200:
            print 'ERR code '+str(resp.status_code)
            return None

        json_data = json.loads(resp.text)
        return json_data        

    def get_object_url(self, url, object_id):
        return self.domain + url + str(object_id) + '/?format=json&access_token=' + self.access_token

    def get_object_data(self, url, object_id):
        resp = requests.get(self.get_object_url(url, object_id))

        if resp.status_code!=200:
            print 'ERR code '+str(resp.status_code)
            return None
           
        json_data = json.loads(resp.text)
        return json_data

    def patch_object(self, url, object_id, field, value):
        object_url = self.get_object_url(url, object_id)
        body = json.dumps({field: value})
        r = requests.patch(url=object_url, data=body, headers={'Content-Type': "application/json"})
        print r.status_code        

class BaserideVehicleApi(BaserideApi):

    def set_base_url(self):
        self.base_url = 'api/v2/transport/vehicle/'

class BaserideServletServletApi(BaserideApi):

    def set_base_url(self):
        self.base_url = 'api/v2/servlet/servlet/'
