#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from wtforms import Form
from niuhe.utils.import_utils import import_types

import_types(file_suffix = '_forms', target_type = Form)
