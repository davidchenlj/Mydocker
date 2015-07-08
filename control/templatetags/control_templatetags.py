# -*- coding: utf-8 -*-
import re, time, os, datetime
from django import template
register = template.Library()

def containers_status(data):
    match=re.search('Exited', data)
    if match:
        return "no"
    else:
        return "ok"

def print_timestamp(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(timestamp)))

def print_size_m(_size):
    return '%.1fM' % float(float(_size) / 1024 / 1024)

def print_tag_name(value):
    return value.split(':')[0]

def print_tag(value):
    return value.split(':')[1]

def print_containers_name(value):
    return value[1:]

register.filter(print_containers_name)
register.filter(print_tag)
register.filter(print_tag_name)
register.filter(print_size_m)
register.filter(containers_status)
register.filter(print_timestamp)