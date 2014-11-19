#!/usr/bin/env python
#!-*- coding: utf-8 -*-

import pymongo
from .fields import BasicField
from .operators import *

class Query(object):
    ASC = pymongo.ASCENDING
    DESC = pymongo.DESCENDING

    def _str_to_field(self, field):
        if not hasattr(self._model_cls, field):
            raise AttributeError('Model class %s has not attribute %s' % (model_cls.__name__, field))
        f = getattr(self._model_cls, field)
        if not isinstance(f, BasicField):
            raise AttributeError('%s is not a field' % field)
        return f

    def __init__(self, db, model_cls, fields):
        model_cls.get_fields()
        self._db = db
        self._table_name = model_cls.collection_name()
        self._table = db[self._table_name]
        self._model_cls = model_cls
        self._fields = []
        self._orders = []
        for field in fields:
            if field is None:
                continue
            elif isinstance(field, BasicField):
                self._fields.append(field)
            elif isinstance(field, str):
                f = self._str_to_field(field)
                self._fields.append(f)
            else:
                raise AttributeError('%s is not a field' % str(field))
        self._filters = []
        self._skip = 0
        self._limit = -1

    def filter(self, *conditions):
        self._filters += conditions
        return self

    def order_by(self, field, direct = None):
        if isinstance(field, str):
            field = self._str_to_field(field)
        if direct is None:
            direct = self.ASC
        self._orders.append((field, direct))
        return self

    def __getitem__(self, index):
        if isinstance(index, int):
            self._skip = index
            self._limit = 1
            try:
                return iter(self).next()
            except StopIteration:
                return None
        elif isinstance(index, slice):
            self._skip = index.start
            self._limit = index.stop - index.start
            return self.all()
        else:
            raise AttributeError('index of query must be int or slice')

    def _get_find_iter(self):
        find_args = []
        find_kwargs = {}
        if self._filters:
            condition = And(*self._filters)
            filter_dict = {}
            condition.to_dict(filter_dict)
            find_args.append(filter_dict)
        if self._fields:
            find_kwargs['fields'] = [field.name for field in self._fields]
        iterator = self._table.find(*find_args, **find_kwargs)
        if self._skip > 0:
            iterator = iterator.skip(self._skip)
        if self._limit >= 0:
            iterator = iterator.limit(self._limit)
        if self._orders:
            sort_data = [(field.name, direct) for field, direct in self._orders]
            print sort_data
            iterator = iterator.sort(sort_data)
        return iterator

    def __iter__(self):
        iterator = self._get_find_iter()
        for item in iterator:
            yield self._model_cls.from_bson_data(item)

    def count(self):
        return self._get_find_iter().count()

    def count_if(self, *condition):
        return self.filter(*condition).count()

    def first(self):
        return self[0]

    def get_first(self, *conditions):
        return self.filter(*conditions)[0]

    def all(self):
        return list(iter(self))

    def get_all(self, *conditions):
        return self.filter(*conditions).all()

    def update(self, *update_ops):
        condition = And(*self._filters)
        filter_dict = {}
        condition.to_dict(filter_dict)
        op_dict = {}
        for op in update_ops:
            op.to_dict(op_dict)
        self._table.update(filter_dict, op_dict)
        return self

