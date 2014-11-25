#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import sys
import os
import os.path as osp
import json
import random
import logging
reload(sys)
sys.setdefaultencoding('u8')
from mako.template import Template
from mako.lookup import TemplateLookup
from utils import *

TEMPLATE_ROOT = osp.join(osp.dirname(osp.abspath(__file__)), 'gen_proj_tpls')

template_lookup = TemplateLookup(
    directories = [TEMPLATE_ROOT],
    input_encoding  = 'utf-8',
    output_encoding = 'utf-8',
)

def create_file_by_template(target_path, template_path, force_rewrite = True, **kwargs):
    if isinstance(target_path, (tuple, list)):
        target_path = osp.join(*target_path)
    if isinstance(template_path, (tuple, list)):
        template_path = osp.join(*template_path)
    if not force_rewrite and osp.exists(target_path):
        logging.info('目标%s已存在，跳过生成', target_path)
        return
    template = template_lookup.get_template(template_path)
    with file(target_path, 'w') as target_file:
        target_file.write(template.render(**kwargs))
    logging.info('生成%s完成', target_path)

def gen_proj_root(proj_name, modules):
    logging.info('正在生成项目根目录...')
    mkdir_p(proj_name)
    mkdir_p(proj_name, 'lib')
    mkdir_p(proj_name, 'doc')

    create_file_by_template(
        target_path     = [proj_name, 'run.py',],
        template_path   = 'run.py.tpl',
    )
    create_file_by_template(
        target_path     = [proj_name, 'run_gevent.py',],
        template_path   = 'run_gevent.py.tpl',
    )
    create_file_by_template(
        target_path     = [proj_name, 'devrun.sh',],
        template_path   = 'devrun.sh.tpl',
    )
    create_file_by_template(
        target_path     = [proj_name, 'config.py',],
        template_path   = 'config.py.tpl',
        secret_key      = ''.join([random.choice('1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM~!@#$%^&*(((()_+-=') for _ in xrange(32)])
    )

def gen_sub_dir(proj_name, mod, mod_type, dirname, suffix):
    if not osp.isdir(osp.join(TEMPLATE_ROOT, 'app', mod_type, dirname)):
        return
    mkdir_p(proj_name, 'app', mod, dirname)
    create_file_by_template(
        target_path     = [proj_name, 'app', mod, dirname, '__init__.py',],
        template_path   = ['app', mod_type, dirname, '__init__.py.tpl'],
        force_rewrite   = False,
    )
    create_file_by_template(
        target_path     = [proj_name, 'app', mod, dirname, 'sample_%s.py' % suffix,],
        template_path   = ['app', mod_type, dirname, 'sample_%s.py.tpl' % suffix],
        force_rewrite   = False,
    )

def gen_module(proj_name, mod, mod_type):
    logging.info('正在生成模块%s...', mod)

    mkdir_p(proj_name, 'app', mod)
    copy_dir(
        osp.join(TEMPLATE_ROOT, 'app', mod_type, 'templates'),
        osp.join(proj_name, 'app', mod, 'templates',),
    )
    copy_dir(
        osp.join(TEMPLATE_ROOT, 'app', mod_type, 'static'),
        osp.join(proj_name, 'app', mod, 'static',),
    )

    create_file_by_template(
        target_path     = [proj_name, 'app', mod, '__init__.py',],
        template_path   = ['app', mod_type, '__init__.py.tpl'],
        mod             = mod,
        proj            = proj_name,
    )

    gen_sub_dir(proj_name, mod, mod_type, 'views', 'views')
    gen_sub_dir(proj_name, mod, mod_type, 'protos', 'protos')
    gen_sub_dir(proj_name, mod, mod_type, 'services', 'services')
    gen_sub_dir(proj_name, mod, mod_type, 'forms', 'forms')
    gen_sub_dir(proj_name, mod, mod_type, 'models', 'models')


def gen_app_with_modules(proj_name, modules):
    logging.info('带模块app...')

    real_modules = []
    for mod in modules:
        if mod.endswith(':api'):
            mod_type = 'mod_api'
            mod = mod[:-4]
        elif mod.endswith(':admin'):
            mod_type = 'mod_admin'
            mod = mod[:-6]
        else:
            mod_type = 'mod'
        real_modules.append(mod)
        gen_module(proj_name, mod, mod_type)

    create_file_by_template(
        target_path     = [proj_name, 'app', '__init__.py',],
        template_path   = ['app', '__init_with_modules__.py.tpl'],
        modules         = real_modules,
    )
    copy_dir(
        osp.join(TEMPLATE_ROOT, 'app', 'static'),
        osp.join(proj_name, 'app', 'static',),
    )

    mkdir_p(proj_name, 'app', '_common')
    create_file_by_template(
        target_path     = [proj_name, 'app', '_common', '__init__.py',],
        template_path   = ['app', '_common', '__init__.py.tpl'],
    )
    gen_sub_dir(proj_name, '_common', '_common', 'consts', 'consts')
    gen_sub_dir(proj_name, '_common', '_common', 'forms', 'forms')
    gen_sub_dir(proj_name, '_common', '_common', 'models', 'models')
    gen_sub_dir(proj_name, '_common', '_common', 'services', 'services')

    mkdir_p(proj_name, 'app', '_common', 'templates')

def gen_app(proj_name, modules):
    logging.info('正在生成app目录,模块个数%d', len(modules))
    mkdir_p(proj_name, 'app')
    return gen_app_with_modules(proj_name, modules)

logging.basicConfig(
    level   = logging.DEBUG,
    format  = '%(asctime)s|%(levelname)s|%(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
)

proj_name = sys.argv[1]
modules = sys.argv[2:]

if not modules:
    logging.error('请指定至少一个模块')
    sys.exit(-1)

gen_proj_root(proj_name, modules)
gen_app(proj_name, modules)
