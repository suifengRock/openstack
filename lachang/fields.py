import bson.objectid
from .operators import *

class BasicField(object):
    def __init__(self, name = None, default_value = None, label = None, widget = None, validators = []):
        self.name = name
        self.field_name = None
        self._default_value = default_value
        self._label = label
        self._validators = validators

    def __get__(self, model, model_type = None):
        if model is not None:
            return model.get(self.field_name, self._default_value)
        else:
            return self

    def __set__(self, model, value):
        if model is not None:
            model[self.field_name] = value

    def __eq__(self, other):
        return SingleCondition(self, Condition.EQ, other)

    def __ne__(self, other):
        return SingleCondition(self, Condition.NE, other)

    def __lt__(self, other):
        return SingleCondition(self, Condition.LT, other)

    def __gt__(self, other):
        return SingleCondition(self, Condition.GT, other)

    def __le__(self, other):
        return SingleCondition(self, Condition.LTE, other)

    def __ge__(self, other):
        return SingleCondition(self, Condition.GTE, other)

    def is_in(self, *values):
        return SingleCondition(self, Condition.IN, values)

    def is_not_in(self, *values):
        return SingleCondition(self, Condition.NOT_IN, values)

    def parse(self, value):
        return value

    def serialize(self, value):
        return value

    def set(self, value):
        return UpdateOp(self, UpdateOp.SET, value)

class ObjIdField(BasicField):
    def parse(self, value):
        return str(value)

    def serialize(self, value):
        return bson.objectid.ObjectId(value)

class IntField(BasicField):
    def parse(self, value):
        return int(value)

    def serialize(self, value):
        return int(value)

    def inc(self, value):
        return UpdateOp(self, UpdateOp.INC, int(value))

    def dec(self, value):
        return UpdateOp(self, UpdateOp.DEC, int(value))

class FloatField(BasicField):
    def parse(self, value):
        return float(value)

    def serialize(self, value):
        return float(value)

class StrField(BasicField):
    def regex(self, pattern):
        return SingleCondition(self, Condition.REGEX, pattern)

class BoolField(BasicField):
    pass

class DictField(BasicField):
    pass

class ListField(BasicField):
    pass

class AnyField(BasicField):
    def serialize(self, value):
        try:
            return int(value)
        except:
            try:
                return float(value)
            except:
                return str(value)
        

class ModelField(BasicField):
    def __init__(self, **kwargs):
        if 'item_field_cls' not in kwargs:
            raise ValueError('item_field_cls cannot be None')
        self._item_field_cls = kwargs.pop('item_field_cls')
        super(ModelField, self).__init__(**kwargs)

    def parse(self, value):
        return self._item_field_cls.from_bson_data(value)

    def serialize(self, value):
        return self._item_field_cls.to_bson_data(value)

class ListModelField(BasicField):
    def __init__(self, **kwargs):
        if 'item_field_cls' not in kwargs:
            raise ValueError('item_field_cls cannot be None')
        kwargs['default_value'] = kwargs.get('default_value', [])
        self._item_field_cls = kwargs.pop('item_field_cls')
        super(ListModelField, self).__init__(**kwargs)

    def parse(self, value):
        return [self._item_field_cls.from_bson_data(item) for item in value]

    def serialize(self, value):
        return [self._item_field_cls.to_bson_data(item) for item in value]

class KeyModelField(BasicField):
    def __init__(self, **kwargs):
        if 'item_field_cls' not in kwargs:
            raise ValueError('item_field_cls cannot be None')
        self._item_field_cls = kwargs.pop('item_field_cls')
        kwargs['default_value'] = kwargs.get('default_value', {})
        super(KeyModelField, self).__init__(**kwargs)

    def parse(self, value):
        return dict([(k, self._item_field_cls.from_bson_data(item))
                        for k, item in value.iteritems()])

    def serialize(self, value):
        return dict([(k, self._item_field_cls.to_bson_data(item))
                        for k, item in value.iteritems()])

class DocField(BasicField):
    def __init__(self, name = None, default_value = None, item_field_cls = None):
        super(DocField, self).__init__(name, default_value)
        if item_field_cls is None:
            raise ValueError('item_field_cls cannot be None')
        self._item_field_cls = item_field_cls

    def parse(self, value):
        return self._item_field_cls.from_bson_data(value)

    def serialize(self, value):
        return self._item_field_cls.to_bson_data(value)

