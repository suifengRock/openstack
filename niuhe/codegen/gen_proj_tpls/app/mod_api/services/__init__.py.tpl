#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from app._common.services import BaseService
from niuhe.utils.import_utils import import_types

import_types(file_suffix = '_services', target_type = BaseService)
