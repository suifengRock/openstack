#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import app
if hasattr(app, 'db'):
    from niuhe.utils.import_utils import import_types
    import_types(
        file_suffix = '_models',
        target_type = app.db.Model,
    )
