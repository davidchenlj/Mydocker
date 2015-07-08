#from django.conf.urls.defaults import *
from django.conf.urls import include, url, patterns

urlpatterns = patterns('control.views',
    url(r'^index/$', 'index', {'template_name':'index.html'}, name='index'),
    url(r'^containers_action/$', 'containers_action', name='containers_action'),
    url(r'^images_list/$', 'images_list', {'template_name':'images_list.html'}, name='images_list'),
    url(r'^inspect_container/(\w+)$', 'inspect_container', {'template_name':'inspect_container.html'}, name='inspect_container'),
    url(r'^create_containers/$', 'create_containers', name='create_containers'),
    url(r'^get_images_list/$', 'get_images_list', name='get_images_list'),
)
