#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from flask import Flask
import config

app = Flask(__name__)
if hasattr(config, 'SECRET_KEY'):
    app.secret_key = config.SECRET_KEY 

if hasattr(config, 'SQLALCHEMY_DATABASE_URI'):
    from flask.ext.sqlalchemy import SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    db = SQLAlchemy(app)

% for mod in modules:
from ${mod} import module as ${mod}_modules
app.register_blueprint(${mod}_modules, url_prefix = '/${mod}')

% endfor

% if 'api' in modules:
if config.DEBUG:
    from niuhe.views.webapi import install_api_list
    install_api_list(app, '/apilist/')
% endif

