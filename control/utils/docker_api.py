# -*- coding: utf-8 -*-
import urllib
import urllib2
import json

domain='http://10.0.2.23:4243'

def docker_api(url, json_data):
    req = urllib2.Request(domain + url, json.dumps(json_data))
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req).read()
    try:
        res_data=json.loads(response)
        return res_data
    except:
        return response

def docker_api_get(url):
    return urllib2.urlopen(domain + url).read()

def docker_api_del(url, json_data):
    request = urllib2.Request(domain + url, json.dumps({}))
    request.get_method = lambda: 'DELETE' # or 'DELETE'
    response = urllib2.urlopen(request)
    return response.read()
