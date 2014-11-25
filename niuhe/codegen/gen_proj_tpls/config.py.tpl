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

SECRET_KEY = '${secret_key}'

SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/demo'

logging.basicConfig(
    level   = logging.DEBUG if DEBUG else logging.INFO,
    format  = '%(asctime)s|%(levelname)s|%(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
)

import sys
for index, directory in enumerate(EXTENTIONS_DIRECTORIES):
    sys.path.insert(index + 1, directory)
