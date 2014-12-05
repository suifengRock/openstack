#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from niuhe.views.dispatch_view import DispatchView, install_to
from niuhe.views.admin.simple_crud_view import get_crud_base_view
from niuhe.utils.import_utils import import_types

import app
from .. import module, render_template

if hasattr(app, 'db'):

    @module.route('/create_db/')
    def create_db():
        from app._common.models import *
        from ..models import *
        app.db.create_all()
        return 'OK'

    AdminDispatchView = get_crud_base_view(app.db, render_template)
    import_types(
        file_suffix = '_views',
        target_type = DispatchView,
        decorators = [
            install_to(module),
        ],
    )
