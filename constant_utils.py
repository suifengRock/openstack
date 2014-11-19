#!-*- coding=utf-8 -*-

import inspect
import collections
import threading

class Item(object):
    def __init__(self, value, title):
        self._value = value
        self._title = title

    @property
    def value(self):
        return self._value

    @property
    def title(self):
        return self._title

    def __get__(self, obj, cls):
        return self._value


class ConstGroup(object):
    @classmethod
    def _get_title_map(cls):
        if not hasattr(cls, '__title_map__'):
            if not hasattr(cls, '__title_map__'):
                cls.__title_map__ = collections.OrderedDict()
                for field, _ in inspect.getmembers(cls):
                    field_obj = cls.__dict__.get(field, None)
                    if isinstance(field_obj, Item):
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
        return cls._get_title_map().items()


if '__main__' == __name__:
    import sys
    reload(sys)
    sys.setdefaultencoding('u8')

    class OrderStatus(ConstGroup):
        UNPAY   = Item(1,   '未支付')
        PAID    = Item(2,   '已支付')
        FINISH  = Item(10,  '已完成')

    print OrderStatus.UNPAY
    print OrderStatus.__dict__['UNPAY'].title

    status = OrderStatus.PAID
    print OrderStatus.get_title(status, 'xx')

    
    print 'All test are passed!'
