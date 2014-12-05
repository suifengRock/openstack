#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import keystoneclient.v2_0.client as ksclient
keystone = ksclient.Client(auth_url="http://192.168.1.200:5000/v2.0",
                           username="xiong",
                           password="123456",
                           tenant_name="admin")
userList = keystone.users.list()
role = keystone.roles.list()

print userList[0]
print userList[0].username



# glance_service = keystone.services.create(name="glance",
                            # service_type="image",
                            # description="OpenStack Image Service")
glance_endpoint = keystone.service_catalog.url_for(service_type='identity',
                                                   endpoint_type='publicURL')
print glance_endpoint

glance_endpoint = keystone.service_catalog.url_for(service_type='identity',
                                                   endpoint_type='internalURL')
print glance_endpoint

glance_endpoint = keystone.service_catalog.url_for(service_type='identity',
                                                   endpoint_type='adminURL')
print glance_endpoint


def get_keystone_creds():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d

def get_nova_creds():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d