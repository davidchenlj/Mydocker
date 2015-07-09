# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import dispatcher

class env_logs(models.Model):
    ''' 容器列表 '''
    create_time=models.CharField(max_length=255)
    container=models.CharField(max_length=255)
    docker_vm=models.CharField(max_length=255)
    type=models.CharField(max_length=255)
    tags=models.CharField(max_length=255)

class containers(models.Model):
    ''' 容器列表 '''
    containers_id=models.CharField(max_length=255, unique=True)
    name=models.CharField(max_length=255)
    status=models.CharField(max_length=255)
    command=models.CharField(max_length=255)
    images=models.CharField(max_length=255)
    host=models.CharField(max_length=255)
    create_time=models.CharField(max_length=255)

def create_env_logs(sender, instance, signals=None, **kwargs):
    print instance

pre_save.connect(create_env_logs, sender=containers)

class docker_vm(models.Model):
    ''' Host主机列表 '''
    docker_addr=models.CharField(max_length=255, unique=True)
    docker_name=models.CharField(max_length=255, blank=True, null=True)
    docker_version=models.CharField(max_length=50, blank=True, null=True)
    kernel_version=models.CharField(max_length=100, blank=True, null=True)
    go_version=models.CharField(max_length=50, blank=True, null=True)
    api_version=models.CharField(max_length=50, blank=True, null=True)

class imgaes(models.Model):
    ''' 容器列表 '''
    images_id=models.CharField(max_length=255, blank=True, null=True)
    name=models.CharField(max_length=255, blank=True, null=True)
    tag=models.CharField(max_length=255, blank=True, null=True)
    host=models.CharField(max_length=255, blank=True, null=True)
    create_time=models.CharField(max_length=255, blank=True, null=True)
    virtualsize=models.CharField(max_length=255, blank=True, null=True)

