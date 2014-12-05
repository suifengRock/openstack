#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import sys
sys.path.append("/Users/suifengluo/Documents/gitlab_work/pycomm")


import os.path as osp
from flask import Blueprint, url_for, request, get_flashed_messages, g
from mako.lookup import TemplateLookup
from niuhe.views.admin.simple_crud_view import TEMPLATE_DIRECTORIES
import config

module = Blueprint('admin', __name__)

_mod_template_directory = osp.join(
    osp.abspath(osp.dirname(__file__)),
    'templates',
)

_common_template_directory = osp.join(
    osp.abspath(osp.dirname(__file__)),
    '..',
    '_common',
    'templates',
)

_template_directories = [
    _mod_template_directory,
    _common_template_directory,
]
_template_directories += config.TEMPLATE_CONFIG['template_additional_paths']
_template_directories += TEMPLATE_DIRECTORIES

_tpl_lookup = TemplateLookup(
    directories     = _template_directories,
    input_encoding  = 'utf-8',
    output_encoding = 'utf-8',
)

def render_template(template_name, **kwargs):
    template = _tpl_lookup.get_template(template_name)
    params = dict(
        url_for = url_for,
        request = request,
        get_flashed_messages = get_flashed_messages,
        g = g,
    )
    params.update(kwargs)
    return template.render(**params)

from .views import *

