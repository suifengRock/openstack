#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import logging
import os.path as osp

PROJECT_ROOT = osp.dirname(osp.abspath(__file__))

EXTENTIONS_DIRECTORIES = [
]

DEBUG = True

TEMPLATE_CONFIG = dict(
    template_additional_paths = [
    ],
)

SVR_CONFIG = dict(
    host    = '127.0.0.1',
    port    = 56789,
    debug   = DEBUG,
)

SECRET_KEY = '7cQex8L&QrujfDs20X1zieS*h2&oDBjl'

SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/test'

import sys
if len(sys.argv) > 1:
    import json
    with file(sys.argv[1]) as config_file:
        config_content = json.load(config_file)
        locals().update(config_content)

logging.basicConfig(
    level   = logging.DEBUG if DEBUG else logging.INFO,
    format  = '%(asctime)s|%(levelname)s|%(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
)

import sys
for index, directory in enumerate(EXTENTIONS_DIRECTORIES):
    sys.path.insert(index + 1, directory)
