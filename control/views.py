# Create your views here.
# -*- coding: utf-8 -*-
import os, sys, commands, re, time, json, simplejson
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader, Context
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.http import HttpResponse
from control.utils.docker_api import docker_api, docker_api_get, docker_api_del

def index(request, template_name):
    res=json.loads(docker_api_get('/containers/json?all=1'))
    t = loader.get_template(template_name)
    c = Context({'containers_list':res, 'request':request})
    return HttpResponse(t.render(c))

def containers_action(request):
    containers_id=request.POST.get('containers_id')
    action=request.POST.get('action')
    try:
        if action == "remove_container":
            docker_api_del('/containers/' + containers_id, json.dumps({}))
        else:
            res_data=docker_api('/containers/%s/%s' % (containers_id, action), {})
    except Exception as error:
        return HttpResponse(str(error))
    return HttpResponse("ok")

def images_list(request, template_name):
    res=json.loads(docker_api_get('/images/json'))
    t = loader.get_template(template_name)
    c = Context({'containers_list':res, 'request':request})
    return HttpResponse(t.render(c))

def get_images_list(request):
    res=json.loads(docker_api_get('/images/json'))
    img_html=''
    for n in res:
        for row in n['RepoTags']:
            _images_name='%s:%s' % (row.split(':')[0], row.split(':')[1])
            html='<option value="%s">%s</option>' % (_images_name, _images_name)
            img_html = img_html + html
    return HttpResponse(img_html)

def inspect_container(request, id, template_name):
    res=json.loads(docker_api_get('/containers/%s/json' % id))
    t = loader.get_template(template_name)
    c = Context({'inspect_data':res, 'request':request, 'active':"yes"})
    return HttpResponse(t.render(c))

def create_containers(request):
    ''' 创建容器 '''
    data=simplejson.loads(request.body)

    # 单个端口与多个端口映射
    PortBindings={}
    ExposedPorts={}
    if isinstance(data['port'], str):
        port_key='%s/%s' % (data['port'], data['protocol'])
        PortBindings[port_key]=[{'HostPort': data['HostPort']}]
        ExposedPorts[port_key]={}
    else:
        for n in range(len(data['port'])):
            port_key='%s/%s' % (data['port'][n], data['protocol'][n])
            PortBindings[port_key]=[{'HostPort': data['HostPort'][n]}]
            ExposedPorts[port_key]={}

    # 创建容器默认参数
    json_create={
        "Name ": 'xiaohuang',
        "Memory": 0,
        "MemorySwap": 0,
        "CpuShares": 512,
        "Cpuset": "0,1",
        "AttachStdin": False,
        "AttachStdout": True,
        "AttachStderr": True,
        "Tty": True,
        "OpenStdin": False,
        "StdinOnce": False,
        "Env": ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],
        "Cmd": [data['command']],
        "Image": data['image'],
        "NetworkDisabled": False,
        "MacAddress": None,
        "SecurityOpts": [""],
        "ExposedPorts": ExposedPorts,
        "HostConfig": {
            "PortBindings": PortBindings,
            "PublishAllPorts": False,
            "Privileged": False,
            "Dns": ["8.8.8.8"],
            "ExtraHosts": None,
            "CapAdd": ["NET_ADMIN"],
            "CapDrop": ["MKNOD"],
            "RestartPolicy": { "Name": "always", "MaximumRetryCount": 0 },
            "NetworkMode": "bridge",
        }
    }

    try:
        # 创建容器
        res_data=docker_api('/containers/create', json_create)
        docker_api('/containers/create', json_create)
        # 修改容器名称
        urls='/containers/%s/rename?name=%s' % (res_data["Id"], data["name"])
        docker_api(urls, {})
    except Exception as error:
        return HttpResponse(str(error))
    return HttpResponse('ok')