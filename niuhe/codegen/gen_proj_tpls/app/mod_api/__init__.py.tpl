#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from flask import Blueprint

module = Blueprint('${mod}', __name__)

from .views import *

