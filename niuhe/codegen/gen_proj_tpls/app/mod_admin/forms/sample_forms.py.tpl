#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from wtforms import Form, validators, TextField
from niuhe.views.zp_forms import EnumSelectField
from app._common.consts import SampleConstGroup

class SampleForm(Form):
    sn          = TextField('例子编号',
                    validators = [
                        validators.Required(
                            message = '例子编号不能为空',
                        ),
                        validators.Regexp(
                            regex   = r'^[\da-zA-Z]{10}$',
                            message = '例子编号应为10位数字或字母',
                        ),
                    ],
                  )
    category    = EnumSelectField('例子分类',
                    group = SampleConstGroup,
                  )
    title       = TextField('标题',
                    validators = [
                        validators.Required(
                            message = '例子编号不能为空',
                        ),
                        validators.Length(
                            min     = 1,
                            max     = 128,
                            message = '标题应为1-128个字符',
                        )
                    ]
                  )
                    
