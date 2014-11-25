#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from niuhe.utils.constant_utils import ConstGroup
from niuhe.utils.import_utils import import_types

import_types(file_suffix = '_consts', target_type = ConstGroup)

