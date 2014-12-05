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
    name        = TextField('名称')


class UserForm(Form):
    username = TextField('用户名',
                validators = [
                    validators.Required(
                        message = '用户名不能为空',
                    ),
                    validators.Regexp(
                        regex = r'^[\dz-zA-Z]{5,10}$',
                        message = '用户名应为5至10位的字母或者数字',
                    ),
                ],)
    email = TextField('邮箱',
            validators = [
                validators.Regexp(
                    regex = r'^[0-9a-zA-Z]+@(([0-9a-zA-Z]+)[.])+[a-z]{2,4}$',
                    message = "请输入正确的邮箱格式",
                ),
            ],)
    password = TextField('密码',
                validators = [
                    validators.Required(
                        message = "密码不能为空",
                    ),
                ],)
                    
