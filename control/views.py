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
from control.models import containers, docker_vm, imgaes


def add_docker_containers(url, docker_addr, c_id=''):
    ''' 添加容器 '''
    try:
        res=json.loads(docker_api_get(url, host=docker_addr))
    except Exception as error:
        error_tmp=str(error).replace("<", "&#60;")
        error_tmp=error_tmp.replace(">", "&#62;")
        return HttpResponse(error_tmp)

    for n in res:
        if c_id and n['Id'] != c_id:
            continue

        match=re.search('Exited', n['Status'])
        containers_status='start'
        if n['Status']:
            if match:
                containers_status="stop"
        else:
            containers_status="stop"

        containers.objects.create(
            containers_id=n['Id'],
            name=n['Names'][0][1:],
            status=containers_status,
            command=n['Command'],
            images=n['Image'],
            host=docker_addr,
            create_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(n['Created'])))
        )


def index(request, template_name):
    queryset=containers.objects.all()
    queryset_docker_vm=docker_vm.objects.all()
    t = loader.get_template(template_name)
    c = Context(
            {
            'queryset':queryset,
            'queryset_docker_vm':queryset_docker_vm,
            'request':request
        }
    )
    return HttpResponse(t.render(c))

def containers_action(request):
    containers_id=request.POST.get('containers_id')
    action=request.POST.get('action')
    queryset=containers.objects.get(containers_id=containers_id)

    code={
        '204':'操作成功!',
        '304':'容器已经启动.',
        '404':'找不到这个容器,或者从来没有启动过.',
        '500 ':'server error',
    }

    try:
        if action == "remove_container":
            docker_api_del('/containers/' + containers_id + '?force=1', json.dumps({}), host=queryset.host)
            containers.objects.filter(containers_id=containers_id).delete()
        else:
            res_data=docker_api('/containers/%s/%s' % (containers_id, action), {}, host=queryset.host)

    except Exception as error:
        status_re=re.search('(\d+)', str(error))
        if status_re:
            status_value=status_re.group(1)
            if code.has_key(status_value):
                if status_value == '304':
                    containers.objects.filter(containers_id=containers_id).update(status=action)
                    return HttpResponse('ok')

            if status_value == '404':
                res_error=json.loads(docker_api_get('/containers/%s/json' % containers_id, host=queryset.host))
                if res_error['State']['Error']:
                    return HttpResponse(res_error['State']['Error'])
                else:
                    return HttpResponse(code['404'])

            return HttpResponse(code[status_value])
        return HttpResponse(str(error))

    if action in ['start', 'stop']:
        containers.objects.filter(containers_id=containers_id).update(status=action)
    return HttpResponse("ok")

def images_list(request, template_name):
    queryset=docker_vm.objects.all()
    def add_images(res, host):
        for n in res:
            for row in n['RepoTags']:
                virtual_size='%.1fM' % float(float(n['VirtualSize']) / 1024 / 1024)
                imgaes.objects.create(
                    images_id=n['Id'],
                    name=row.split(':')[0],
                    tag=row.split(':')[1],
                    host=host,
                    create_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(n['Created']))),
                    virtualsize=virtual_size,
                )

    if request.POST:
        imgaes.objects.all().delete()
        for host in queryset:
            res=json.loads(docker_api_get('/images/json', host=host.docker_addr))
            add_images(res, host.docker_addr)
        return HttpResponse('ok')

    t = loader.get_template(template_name)
    c = Context({'containers_list':imgaes.objects.all(), 'request':request})
    return HttpResponse(t.render(c))

def get_images_list(request):
    docker_host=request.POST.get('docker_host')
    res=imgaes.objects.filter(host=docker_host)
    img_html=''
    for n in res:
        _images_name='%s:%s' % (n.name, n.tag)
        html='<option value="%s">%s</option>' % (_images_name, _images_name)
        img_html = img_html + html
    return HttpResponse(img_html)

def inspect_container(request, id, template_name):
    queryset=containers.objects.get(containers_id=id)
    res=json.loads(docker_api_get('/containers/%s/json' % id, host=queryset.host))
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

    code={
        '204':'操作成功!',
        '406':'impossible to attach (container not running).',
        '404':'no such container',
        '409':'conflict name already assigned.',
        '500 ':'server error',
        }

    try:
        # 创建容器
        res_data=docker_api('/containers/create', json_create, host=data['vm_host'])

        # 修改容器名称
        urls='/containers/%s/rename?name=%s' % (res_data["Id"], data["name"])
        docker_api(urls, {}, host=data['vm_host'])

        # 添加容器
        add_docker_containers('/containers/json?all=1' , data['vm_host'], c_id=res_data["Id"])
    except Exception as error:
        status_re=re.search('(\d+)', str(error))
        if status_re:
            status_value=status_re.group(1)
            if code.has_key(status_value):
                return HttpResponse(code[status_value])
        error_tmp=str(error).replace("<", "&#60;")
        error_tmp=error_tmp.replace(">", "&#62;")
        return HttpResponse(str(error_tmp))
    return HttpResponse('ok')

def vm_host_list(request, template_name):
    queryset=docker_vm.objects.all()
    t = loader.get_template(template_name)
    c = Context({'queryset':queryset, 'request':request})
    return HttpResponse(t.render(c))

def add_vm_host(request, template_name):
    if request.POST:
        docker_name=request.POST.get('docker_name')
        docker_addr=request.POST.get('docker_addr')
        docker_update=request.POST.get('docker_update')

        # 更新当前所以容器状态
        if docker_update == "update":
            containers.objects.all().delete()
            for row in docker_vm.objects.all():
                add_docker_containers('/containers/json?all=1', row.docker_addr)
            return HttpResponse('ok')

        # 添加容器
        if docker_update == "add":
            add_docker_containers('/containers/json?all=1', docker_addr)
            version_res=json.loads(docker_api_get('/version', host=docker_addr))
            docker_vm.objects.create(
                docker_name=docker_name,
                docker_addr=docker_addr,
                docker_version=version_res['Version'],
                kernel_version=version_res['KernelVersion'],
                go_version=version_res['GoVersion'],
                api_version=version_res['ApiVersion']
            )
        return HttpResponse('添加成功.')
    t = loader.get_template(template_name)
    c = Context({'request':request})
    return HttpResponse(t.render(c))