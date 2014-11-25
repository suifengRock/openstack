#!/usr/bin/env python
#!-*- coding=utf-8 -*-

from wtforms import Form, validators, TextField, IntegerField,\
                     SelectField, DateField, HiddenField,\
                     PasswordField
from wtforms.compat import text_type, izip
from wtforms.widgets import HTMLString, html_params
from wtforms.utils import unset_value
import time

# Fields

class ZpDateTimeField(IntegerField):
    __DATEFMTS__ = dict(
        DATETIME    = ('zp-datetime-picker', '%Y-%m-%d %H:%M:%S'),
        DATE        = ('zp-date-picker', '%Y-%m-%d'),
    )

    def __init__(self, label = None, format = 'DATETIME', readonly = False, *args, **kwargs):
        super(ZpDateTimeField, self).__init__(label, *args, **kwargs)
        self._readonly = readonly
        self._css_class, self._datetime_fmt = self.__DATEFMTS__[format.upper()]
        
    def __call__(self, *args, **kwargs):
        if self._readonly:
            return '<span>%s</span>' % (self.get_text(kwargs.get('value', self.data)) if self.data else 'N/A')
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
        if 0 == value:
            return ''
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
            
    def validate(self, *args, **kwargs):
        if self._readonly:
            return True
        return super(self, ZpDateTimeField).validate(*args, **kwargs)

class ZpModelSelectField(SelectField):

    no_bootstrap = 1

    def __init__(self, label = None, value_field = None, label_field = None, 
            filters = [], *args, **kwargs):
        self._value_field = value_field
        self._label_field = label_field
        self._filters = filters
        kwargs['choices'] = []
        super(ZpModelSelectField, self).__init__(label, *args, **kwargs)

    def update_choices(self, session):
        q = session.query(self._value_field, self._label_field)
        if self._filters:
            q.filter(*self._filters)
        self.choices = q.all()

    def __call__(self, *args, **kwargs):
        if 'class_' in kwargs:
            kwargs['class_'] += ' zp-select2'
        else:
            kwargs['class_'] = 'zp-select2'
        return super(ZpModelSelectField, self).__call__(*args, **kwargs)

# Widgets

class RadioGroupWidget(object):
    
    def __call__(self, field, **kwargs):
        html = ['<div class="row form-group" style="margin-top: 5px">',]
        for value, text, selected in field.iter_choices():
            html += [
                '<div class="col-sm-3">',
                    '<div class="radio">',
                        '<label>',
                            '<input name="%s" value="%s" type="radio" %s/>%s' % (
                                field.name, str(value), 'checked' if selected else '', text),
                            '<i class="fa fa-circle-o small"></i>',
                        '</label>',
                    '</div>',
                '</div>',
            ]
        html += ['</div>',]
        return HTMLString(''.join(html))


