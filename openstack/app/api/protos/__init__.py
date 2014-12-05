#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from niuhe.protos.messages import Message
from niuhe.utils.import_utils import import_types

import_types(file_suffix = '_protos', target_type = Message)
