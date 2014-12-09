#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import logging
from flask import request, abort
from niuhe.views.dispatch_view import DispatchView, install_to

from .. import render_template

from ..forms import SampleForm
from app._common.models import *

from . import AdminDispatchView
import keystoneclient.v2_0.client as ksclient
import novaclient.v1_1.client as nvclient

print AdminDispatchView
class Sample(AdminDispatchView):
    __title__       = '例子'
    __model_type__  = SampleModel
    __form_type__   = SampleForm


class TestFirst(AdminDispatchView):
    __title__       = '测试1'
    __model_type__  = SampleModel
    __form_type__   = SampleForm


class TestSecond(AdminDispatchView):
    __title__       = '测试2'
    __model_type__  = SampleModel
    __form_type__   = SampleForm
    __skipfields__  = ['name']

class Test(AdminDispatchView):

    list_template = "/test.html"

    def _render(self, tpl_name, **kwargs):
        tpl_kwargs = {}
        tpl_kwargs.update(kwargs)
        return render_template(tpl_name, **tpl_kwargs)

    def list_GET(self):
        if not self._allow_list():
            abort(403)

        return self._render(
            self.list_template,
            title = '测试',
            test = 'python',
            skip_fields = ['name'],
            )
class Dashboard(AdminDispatchView):
    list_template = '/dashboard.html'
    def _render(self, tpl_name, **kwargs):
        tpl_kwargs = {}
        tpl_kwargs.update(kwargs)
        return render_template(tpl_name, **tpl_kwargs)

    def get_nova_creds(self):
        creds = {}
        creds['username'] = 'xiong'
        creds['api_key'] = '123456'
        creds['auth_url'] = 'http://192.168.1.200:5000/v2.0'
        creds['project_id'] = 'admin'
        return creds

    def get_keystone_creds(self):
        d = {}
        d['username'] = 'xiong'
        d['password'] = '123456'
        d['auth_url'] = 'http://192.168.1.200:5000/v2.0'
        d['tenant_name'] = 'admin'
        return d

    def get_service_list(self):
        creds = self.get_keystone_creds()
        keystone = ksclient.Client(**creds)
        return keystone.services.list()

    def get_server_list(self):
        creds = self.get_nova_creds()
        serverList = []
        nova = nvclient.Client(**creds)
        servers = nova.servers.list()
        for obj in servers :
            server = {}
            server['name'] = obj.name
            server['images'] = nova.images.get(obj.image['id']).name
            flavor =  nova.flavors.get(obj.flavor['id'])
            server['flavor_name'] = flavor.name
            server['ram'] = flavor.ram /1024.00
            server['vcpus'] = flavor.vcpus
            server['disk'] = flavor.disk
            server['status'] = obj.status
            serverList.append(server)
        return serverList

    def get_usage_info(self):
        creds = self.get_nova_creds()
        nova = nvclient.Client(**creds)
        servers = nova.servers.list()
        usage_info ={'ram': 0, 'vcpus': 0, 'disk':0 }
        for obj in servers :
            flavor =  nova.flavors.get(obj.flavor['id'])
            usage_info['ram'] += flavor.ram 
            usage_info['vcpus'] += flavor.vcpus
            usage_info['disk'] += flavor.disk

        usage_info['ram'] = usage_info['ram']/1024.00
        return usage_info

    def get_quotas_info(self):
        creds = self.get_nova_creds()
        nova = nvclient.Client(**creds)
        return nova.quotas.get(tenant_id=nova.tenant_id, user_id=nova.user_id)
    
    def list_GET(self):
        if not self._allow_list():
            abort(403)
       
        return self._render(
            self.list_template,
            title = '橄榄',
            serviceList = self.get_service_list(),
            serverList = self.get_server_list(),
            usageInfo = self.get_usage_info(),
            quotasInfo = self.get_quotas_info(),
            )
