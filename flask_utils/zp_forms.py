#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from wtforms import Form, validators, TextField, IntegerField,\
                     SelectField, DateField, HiddenField,\
                     PasswordField
from wtforms.utils import unset_value
import time

class ZpDateTimeField(IntegerField):
    __DATEFMTS__ = dict(
        DATETIME    = ('zp-datetime-picker', '%Y-%m-%d %H:%M'),
        DATE        = ('zp-date-picker', '%Y-%m-%d'),
    )

    def __init__(self, format = 'DATETIME', *args, **kwargs):
        super(ZpDateTimeField, self).__init__(*args, **kwargs)
        self._css_class, self._datetime_fmt = self.__DATEFMTS__[format.upper()]
        
    def __call__(self, *args, **kwargs):
        if 'class_' in kwargs:
            class_list = kwargs['class_'].split()
            if self._css_class not in class_list:
                class_list.append(self._css_class)
                kwargs['class_'] = ' '.join(class_list)
        else:
            kwargs['class_'] = self._css_class
        kwargs['value'] = self.get_text(kwargs.get('value', self.data)) if self.data else ''
        return super(ZpDateTimeField, self).__call__(*args, **kwargs)

    def get_text(self, value):
        return time.strftime(
            self._datetime_fmt,
            time.localtime(float(value)),
        )

    def process_formdata(self, valuelist):
        if valuelist:
            value = valuelist[0]
            if isinstance(value, (str, unicode)):
                ta = time.strptime(value, self._datetime_fmt)
                self.data = int(time.mktime(ta))
            else:
                self.data = int(value)
        else:
            self.data = 0
            
class ZpIntSelectField(SelectField):
    def process_formdata(self, valuelist):
        if valuelist:
            value = valuelist[0]
            self.data = int(value)
        else:
            self.data = self.default
