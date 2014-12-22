#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from app._common.services import BaseService
import keystoneclient.v2_0.client as ksclient
import novaclient.v1_1.client as nvclient


class StackCreds(BaseService):

    __nova_client__

    def __init__(self):
        self.__nova_client__ = self.__connect_nova()
        self.__keystone_client__ = self.__connect_keystone()

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

    def __connect_keystone(self):
        creds = self.get_keystone_creds()
        keystone = ksclient.Client(**creds)
        return keystone

    def __connect_nova(self):
        creds = self.get_nova_creds()
        nova = nvclient.Client(**creds)
        return nova

    def get_keystone_client(self):
        if not self.__nova_client__:
            return self.__nova_client__
        return self.__connect_keystone()

    def get_nova_client(self):
        if not self.__keystone_client__:
            return self.__keystone_client__
        return self.__connect_nova()
