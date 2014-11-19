from lachang import *
import json

class PostLog(Model):
    sim_num         = StrField()
    version_release = StrField()
    send_time       = StrField()
    model           = StrField()
    channel_num     = StrField()
    device_id       = StrField()

    def __repr__(self):
        return '<PostLog: objid=%(obj_id)s, send_time=%(send_time)s>' % self


session = Session('localhost', 27017, 'sms_proxy')

print json.dumps(
        session.query(PostLog
                    ).filter(
                        PostLog.version_release >= '4',
                    ).all(),
        indent = 4
      )

class Member(Model):
    name    = StrField()

class SubConfig(Model):
    time    = IntField()
    name    = StrField()

class Group(Model):
    title   = StrField()
    members = ListModelField(
                item_field_cls = Member,
              )
    leader  = ModelField(
                item_field_cls = Member,
              )
    config  = KeyModelField(
                item_field_cls = Member,
              )
    tags    = ListField()

session = Session('localhost', 27017, 'test_lachang')

g = Group()
g.title = 'Hello'
g.tags = ['computer', 'mobile', 'python']
leader = Member()
leader.name = 'XXXXX'
g.leader = leader
for i in xrange(10):
    m = Member()
    m.name = 'xx_' + str(i)
    g.members.append(m)

for i in xrange(3):
    c = SubConfig()
    c.time = i
    c.name = 'yyy_' + str(i)
    g.config['xxx_' + str(i)] = c

session.add(g)

print json.dumps(session.query(Group, Group.obj_id).order_by(Group.obj_id).all(), indent = 4)
print json.dumps(session.query(Group, Group.obj_id).order_by(Group.obj_id, Query.DESC).all(), indent = 4)
