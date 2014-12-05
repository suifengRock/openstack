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

from admin import module as admin_modules
app.register_blueprint(admin_modules, url_prefix = '/admin')

from api import module as api_modules
app.register_blueprint(api_modules, url_prefix = '/api')


if config.DEBUG:
    from niuhe.views.webapi import install_api_list
    install_api_list(app, '/apilist/')

