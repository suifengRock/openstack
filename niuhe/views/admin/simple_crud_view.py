#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import os.path as osp
import logging
import traceback
from flask import request, flash, redirect, url_for, abort, g
from ..dispatch_view import DispatchView

__all__ = [
    'TEMPLATE_DIRECTORIES',
    'get_crud_base_view',
]

TEMPLATE_DIRECTORIES = [
    osp.join(
        osp.join(osp.abspath(osp.dirname(__file__))),
        '..',
        '..',
        'templates',
    ),
]

def get_crud_base_view(db, render_template):

    class _SimpleCRUDView(DispatchView):

        __scope__           = ()
        __readonly__        = False
        __onlyfields__      = []
        __skipfields__      = []
        __edit_template__   = '/common_edit.html'
        __list_template__   = '/common_list.html'
        __list_args__       = {}
        __list_filters__    = []

        def _readonly(self):
            return self.__readonly__

        def _allow_access(self):
            return True

        def _allow_list(self):
            return self._allow_access()

        def _allow_view(self):
            return self._allow_access()

        def _allow_add(self):
            return self._allow_access()

        def _allow_edit(self):
            return self._allow_access()

        def _allow_del(self):
            return self._allow_access()

        def _get_form(self, *args, **kwargs):
            return self.__form_type__(*args, **kwargs)

        def _iter_pk(self):
            for col in self.__model_type__.__table__.primary_key.columns:
                yield col.name

        def _get_item_from_args(self):
            args = []
            for key in self._iter_pk():
                key_data = request.args.get(key, None)
                if key_data is None:
                    return None
                args.append(key_data)
            return self.__model_type__.query.get(tuple(args))

        def _get_list_filters(self):
            return []

        def _render(self, tpl_name, **kwargs):
            tpl_kwargs = {
                'scope'         : self.__scope__ + (self.__title__,),
                'only_fields'   : self.__onlyfields__, 
                'skip_fields'   : self.__skipfields__,
                'readonly'      : self._readonly(),
                'title'         : '',
            }
            tpl_kwargs.update(kwargs)
            return render_template(tpl_name, **tpl_kwargs)

        def list_GET(self):
            if not self._allow_list():
                abort(403)

            page_size = int(request.args.get('page_size', 10))
            page_index = int(request.args.get('page', '1'))

            filters = self._get_list_filters()
            if filters:
                total = self.__model_type__.query.filter(*filters).count()
            else:
                total = self.__model_type__.query.count()

            max_page = (total + page_size - 1) / page_size
            if max_page < 1:
                max_page = 1
            if page_index < 1:
                page_index = 1
            elif page_index > max_page:
                page_index = max_page

            start = (page_index - 1) * page_size

            if filters:
                items = self.__model_type__.query.filter(*filters).offset(start).limit(page_size)
            else:
                items = self.__model_type__.query.offset(start).limit(page_size)

            return self._render(
                self.__list_template__,
                items       = items,
                total       = total,
                max_page    = max_page,
                page_index  = page_index,
                page_size   = page_size,
                title       = self.__title__ + '列表',
                view_cls    = self.__class__.__name__,
                sample_form = self._get_form(),
                pk_list     = list(self._iter_pk()),
                list_args   = self.__list_args__,
            )

        def add_GET(self):
            if self._readonly():
                abort(404)
            if not self._allow_add():
                abort(403)

            form = self._get_form()
            return render_template(
                self.__edit_template__,
                title   = '新增' + self.__title__,
                form    = form,
            )

        def add_POST(self):
            if self._readonly():
                abort(404)
            if not self._allow_add():
                abort(403)
            form = self._get_form(request.form)
            if not form.validate():
                return self._render(
                    self.__edit_template__,
                    action  = '新建',
                    form    = form,
                )
            item = self.__model_type__(**form.data)
            try:
                db.session.add(item)
                db.session.commit()
                return self._redirect('list', success = '新建%s成功' % self.__title__)
            except Exception, ex:
                traceback.print_exc()
                flash('新建%s失败' % self.__title__, 'error')
                return self._render(
                    self.__edit_template__,
                    title   = '新建' + self.__title__,
                    form    = form,
                )

        def view_GET(self):
            if not self._allow_view():
                abort(403)
            item = self._get_item_from_args()
            if not item:
                abort(404)
            form = self._get_form(obj = item)
            return self._render(
                self.__edit_template__,
                title   = '查看' + self.__title__,
                form    = form,
                readoly = True,
            )

        def edit_GET(self):
            if self._readonly():
                abort(404)
            if not self._allow_edit():
                abort(403)
            item = self._get_item_from_args()
            if not item:
                abort(404)
            form = self._get_form(obj = item)
            return self._render(
                self.__edit_template__,
                title   = '编辑' + self.__title__,
                form    = form,
            )

        def edit_POST(self):
            if self._readonly():
                abort(404)
            if not self._allow_edit():
                abort(403)
            form = self._get_form(request.form)
            if not form.validate():
                return self._render(
                    self.__edit_template__,
                    action  = '编辑',
                    form    = form,
                    title   = '编辑' + self.__title__,
                )
            item = self.__model_type__(**form.data)
            try:
                db.session.merge(item)
                db.session.commit()
                return self._redirect('list', success = '编辑%s成功' % self.__title__)
            except Exception, ex:
                traceback.print_exc()
                flash('编辑%s失败' % self.__title__, 'error')
                return self._render(
                    self.__edit_template__,
                    action  = '编辑',
                    form    = form,
                    title   = '编辑' + self.__title__,
                )

        def del_GET(self):
            if self._readonly():
                abort(404)
            if not self._allow_edit():
                abort(403)
            item = self._get_item_from_args()        
            if item is None:
                abort(404)
            try:
                db.session.delete(item)
                db.session.commit()
                return self._redirect('list', success = '删除成功')
            except Exception, ex:
                traceback.print_exc()
                return self._redirect('list', error = '删除失败')

    return _SimpleCRUDView

