#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import logging
import traceback
from flask import request, abort, flash
from niuhe.views.dispatch_view import DispatchView, install_to

from .. import render_template

from ..forms import SampleForm
from ..forms import ServerListForm, ServerEditForm
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
    __title__          = '主机实例'
    __list_template__  = '/server_list.html'

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

    def get_server_list(self):
        creds = self.get_nova_creds()
        nova = nvclient.Client(**creds)
        servers = nova.servers.list()
        serverList = []
        for obj in servers:
            server = {}
            server['name'] = obj.name
            server['images'] = nova.images.get(obj.image['id']).name
            flavor =  nova.flavors.get(obj.flavor['id'])
           
            ram = str(flavor.ram /1024.00)
            vcpus = str(flavor.vcpus)
            disk = str(flavor.disk)
            server['ram']       = ram+'GB'
            server['vcpu']      = vcpus+'个'
            server['disk']      = disk+'GB'
            server['status']    = obj.status
            serverList.append(server)
        return serverList

    def add_server_service(self, name, image_name, flavor_id):
        creds = self.get_nova_creds()
        nova = nvclient.Client(**creds)
        flavor = nova.flavors.get(flavor_id)
        image = nova.images.find(name=image_name)
        nova.servers.create(name=name, image=image, flavor=flavor)


    def list_GET(self):
        if not self._allow_list():
            abort(403)
        self.__form_type__   = ServerListForm
        serverlist = self.get_server_list()

        return self._render(
            self.__list_template__,
            items = serverlist,
            total = len(serverlist),
            max_page = 1,
            page_index = 1,
            page_size = 1,
            title       = self.__title__,
            view_cls    = self.__class__.__name__,
            sample_form = self._get_form(),
            pk_list     = list(),
            list_args   = self.__list_args__,
            )

    def get_flavor_list(self):
        creds = self.get_nova_creds()
        nova = nvclient.Client(**creds)
        return nova.flavors.list()

    def get_images_list(self):
        creds = self.get_nova_creds()
        nova = nvclient.Client(**creds)
        return nova.images.list()

    def add_GET(self):
        self.__edit_template__   = '/create_server.html'
        self.__form_type__   = ServerEditForm
        
        if self._readonly():
            abort(404)
        if not self._allow_add():
            abort(403)
        form = self._get_form()

        flavorList = self.get_flavor_list()
        imagesList = self.get_images_list()

        return render_template(
            self.__edit_template__,
            title   = '新建' + self.__title__,
            form    = form,
            flavor_list = flavorList,
            images_list = imagesList,
        )

    def add_POST(self):
        if self._readonly():
            abort(404)
        if not self._allow_add():
            abort(403)

        self.__form_type__   = ServerEditForm
        form = self._get_form(request.form)
        if not form.validate():
            return render_template(
                '/create_server.html',
                form = form,
            )

        try:
            self.add_server_service(name=form.data['name'],
                                    image_name=form.data['images'],
                                    flavor_id=form.data['flavor'])
            return  self._redirect('list', success = '新建%s成功' % self.__title__)
        except Exception, ex:
            traceback.print_exc()
            flash('新建%s失败' % self.__title__, 'error')
            return self._render(
                    '/create_server.html',
                    title   = '新建' + self.__title__,
                    form    = form,
                )


class TestSecond(AdminDispatchView):
    __title__       = '主机实例'
    __model_type__  = SampleModel
    __form_type__   = SampleForm



class Test(AdminDispatchView):

    list_template = '/test.html'

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
        usage_info['instances'] = len(servers)
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
