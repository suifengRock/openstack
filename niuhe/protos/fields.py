#!/usr/bin/env python
#!-*- coding=utf-8 -*-

__all__  =[
    'required',
    'optional',
    'repeated',
]

class _LabelType(object):
    REQUIRED = 1
    OPTIONAL = 2
    REPEATED = 3
    NAME     = {
        REQUIRED : '必填',
        OPTIONAL : '选填',
        REPEATED : '数组',
    }

class BasicField(object):
    _type_name = '未知'

    def __init__(self, tag = -1, repeated = False, required = False, desc = ''):
        self._tag = -1
        if repeated:
            self._label = _LabelType.REPEATED
        elif required:
            self._label = _LabelType.REQUIRED
        else:
            self._label = _LabelType.OPTIONAL
        self._desc = desc
        self.name = ''

    @property
    def tag(self):
        return self._tag

    @property
    def label(self):
        return self._label

    @property
    def label_name(self):
        return _LabelType.NAME[self._label] 

    @property
    def type_name(self):
        return self._type_name

    @property
    def required(self):
        return _LabelType.REQUIRED == self._label

    @property
    def repeated(self):
        return _LabelType.REPEATED == self._label

    @property
    def optional(self):
        return _LabelType.OPTIONAL == self._label

    @property
    def desc(self):
        return self._desc

    def __get__(self, obj, cls):
        if obj is None:
            return self
        return obj._field_values[self.name]

    def __set__(self, obj, value):
        if obj is None:
            return
        if self.repeated:
            if not isinstance(value, (list, tuple)):
                raise ValueError(
                    'field %s is repeated, but given value is neither list nor tuple' % self.name)
            obj._field_values[self.name] = [self._parse(item) for item in value]
        else:
            obj._field_values[self.name] = self._parse(value)

    def _is_valid(self, value):
        return True

    def _parse(self, value):
        return value

    def to_dict_value(self, value):
        return value

    def from_dict_value(self, value):
        if self.repeated:
            return [self._parse(item) for item in value]
        else:
            return self._parse(value)

class _NumberField(BasicField):
    pass

class IntegerField(_NumberField):
    _type_name = '整型'
    def _parse(self, value):
        return int(value)

class FloatField(_NumberField):
    _type_name = '浮点型'
    def _parse(self, value):
        return float(value)

class LongField(_NumberField):
    _type_name = '长整型'
    def _parse(self, value):
        return long(value)

class StringField(BasicField):
    _type_name = '字符串'
    def _parse(self, value):
        return str(value)

class BooleanField(BasicField):
    _type_name = '布尔型'
    def _parse(self, value):
        return bool(value)

class MessageField(BasicField):
    def __init__(self, cls = None, **kwargs):
        super(MessageField, self).__init__(**kwargs)
        self._cls = cls

    @property
    def cls(self):
        return self._cls
        
    def new(self, **init_datas):
        return self._cls(**init_datas)

    def to_dict_value(self, value):
        if self.repeated:
            return [item.to_dict() for item in value]
        else:
            return value.to_dict()
        
    def from_dict_value(self, value):
        if self.repeated:
            return [self.new(**item) for item in value]
        else:
            return self.new(**value)
    
    @property
    def type_name(self):
        return '结构体：%s' % self._cls.__name__

class EnumField(IntegerField):

    def __init__(self, group = None, **kwargs):
        super(EnumField, self).__init__(**kwargs)
        self._const_group = group

    @property
    def group(self):
        return self._const_group

    @property
    def desc(self):
        content = super(EnumField, self).desc
        content += '\n取值范围：'
        for value, title in self._const_group.get_title_dict().iteritems():
            content += '%s - %s; ' % (str(value), title)
        return content

class FileField(BasicField):
    _type_name  = '文件' 

class _FieldClassWrapper(object):

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __getattr__(self, name):
        import inspect
        import functools
        mod = inspect.getmodule(type(self))
        field_cls_dict = dict(inspect.getmembers(mod, lambda obj: isinstance(obj, type) and issubclass(obj, BasicField)))
        field_cls = field_cls_dict.get(name, None)
        if not field_cls:
            raise NameError('no field type %s' % name)
        if self._kwargs:
            return functools.partial(field_cls, **self._kwargs)
        else:
            return field_cls

required = _FieldClassWrapper(required = True)

repeated = _FieldClassWrapper(repeated = True)

optional = _FieldClassWrapper()

