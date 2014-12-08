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
# glance_endpoint = keystone.service_catalog.url_for(service_type='identity',
#                                                    endpoint_type='publicURL')
# print glance_endpoint

# glance_endpoint = keystone.service_catalog.url_for(service_type='identity',
#                                                    endpoint_type='internalURL')
# print glance_endpoint

# glance_endpoint = keystone.service_catalog.url_for(service_type='identity',
#                                                    endpoint_type='adminURL')
# print glance_endpoint


def get_keystone_creds():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d

def get_nova_creds():
    d = {}
    d['username'] = "xiong"
    d['api_key'] = "123456"
    d['auth_url'] = "http://192.168.1.200:5000/v2.0"
    d['project_id'] = "admin"
    return d

import novaclient.v1_1.client as nvclient
from  datetime  import  datetime
creds = get_nova_creds()
nova = nvclient.Client(**creds)
print nova.servers.list()
print nova.images.list()
print nova.agents.list()
print nova.services.list()
print nova.limits.get(tenant_id='9bbd825a9ade4860a08b452a41a78da1')
print nova.flavors.list()
print nova.quotas.get(tenant_id='9bbd825a9ade4860a08b452a41a78da1',
						user_id='01057ca6ed074c53842fbf93e2bab949')

print nova.quotas.defaults(tenant_id='9bbd825a9ade4860a08b452a41a78da1')
print nova.usage.get(start=datetime.today(),
						end=datetime.today(),
						tenant_id='9bbd825a9ade4860a08b452a41a78da1')
