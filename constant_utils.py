#!-*- coding=utf-8 -*-

import inspect
import collections

__all__ = [
    'Item',
    'ConstGroup',
]

class Item(object):
    def __init__(self, value, title):
        self._value = value
        self._title = title
        self._key   = ''

    @property
    def value(self):
        return self._value

    @property
    def title(self):
        return self._title

    @property
    def key(self):
        return self._key

    def __get__(self, obj, cls):
        return self._value


class ConstGroup(object):
    @classmethod
    def _get_title_map(cls):
        if not '__title_map__' in cls.__dict__:
            cls.__title_map__ = collections.OrderedDict()
            for field, _ in inspect.getmembers(cls):
                field_obj = cls.__dict__.get(field, None)
                if not isinstance(field_obj, Item):
                    continue
                if field_obj.value in cls.__title_map__:
                    raise ValueError('Duplicated const value %s in group %s' \
                        % (str(field_obj.value), cls.__name__))
                cls.__title_map__[field_obj.value] = field_obj.title
        return cls.__title_map__

    @classmethod
    def get_title(cls, value, default = ''):
        return cls._get_title_map().get(value, default)

    @classmethod
    def get_title_dict(cls):
        return cls._get_title_map()

    @classmethod
    def get_choices(cls):
        choices = cls._get_title_map().items()
        choices.sort(key = lambda item: item[0])
        return choices

    @classmethod
    def has_value(cls, value):
        return value in cls._get_title_map()

if '__main__' == __name__:
    import sys
    reload(sys)
    sys.setdefaultencoding('u8')

    class OrderStatus(ConstGroup):
        UNPAY   = Item(1,   '未支付')
        PAID    = Item(2,   '已支付')
        FINISH  = Item(10,  '已完成')

    assert 1 == OrderStatus.UNPAY
    assert '未支付' == OrderStatus.__dict__['UNPAY'].title

    status = OrderStatus.PAID
    assert '已支付' == OrderStatus.get_title(status, 'cannot get title')

    
    print 'All test are passed!'
