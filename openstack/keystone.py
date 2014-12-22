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
print keystone.tenant_id
print keystone.user_id
print keystone.services.list()



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
# print nova.servers.list()
print nova.images.list()
print nova.agents.list()
print nova.services.list()
print nova.limits.get(tenant_id='9bbd825a9ade4860a08b452a41a78da1')
print nova.flavors.list()
print nova.quotas.get(tenant_id='9bbd825a9ade4860a08b452a41a78da1',
						user_id='01057ca6ed074c53842fbf93e2bab949').cores

print nova.quotas.defaults(tenant_id='9bbd825a9ade4860a08b452a41a78da1')

from novaclient import base
server = nova.servers.list()[0]

print server.name
# server = nova.servers.find(name="spice7")

# print server.flavor['id']

# print nova.servers.get(server)

print server.image
print server.flavor

# print nova.images.get(server.image['id']).name

# flavor =  nova.flavors.get(server.flavor['id'])
flavor = nova.flavors.list()[0]
print flavor.ram
print flavor.name
print flavor.vcpus
print flavor.disk
print server.status

# image = nova.images.find(name="spice7uav")
# flavor = nova.flavors.find(name="m1.small")
# instance = nova.servers.create(name="testPY", image=image, flavor=flavor)
# print instance.status

print nova.flavors.get("1").name




