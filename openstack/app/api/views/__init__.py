#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from niuhe.views.dispatch_view import DispatchView, install_to
from niuhe.utils.import_utils import import_types
from niuhe.views.webapi import webapi_class
from .. import module

import_types(
    file_suffix = '_views',
    target_type = DispatchView,
    decorators = [
        webapi_class(module),
        install_to(module),
    ]
)
