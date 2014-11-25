#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import logging
from flask import request
from niuhe.views.dispatch_view import DispatchView, install_to

from ..forms import SampleForm
from app._common.models import *

from . import AdminDispatchView

print AdminDispatchView
class Sample(AdminDispatchView):
    __title__       = '例子'
    __model_type__  = SampleModel
    __form_type__   = SampleForm

