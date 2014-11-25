#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import logging
from flask import request
from niuhe.views.dispatch_view import DispatchView, install_to

from .. import module, render_template
from ..forms import *
from ..services import *


class Hello(DispatchView):

    def hello_GET(self):
        return render_template(
            'sample_template.html',
            name = request.args.get('name', 'NIUHE'),
        )

