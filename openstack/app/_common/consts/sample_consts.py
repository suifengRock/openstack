#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from niuhe.utils.constant_utils import ConstGroup, Item

class SampleConstGroup(ConstGroup):
    CPP     = Item(1, 'C++')
    PYTHON  = Item(2, 'Python')
    PHP     = Item(3, 'Php')
    GO      = Item(4, 'Go')
