#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import inspect
import json
import functools
import logging
import traceback
import os.path as osp
from mako.lookup import TemplateLookup
from mako.template import Template
from flask import url_for, request, Blueprint, abort
from niuhe.protos.fields import BasicField, MessageField, FileField

__all__ = [
    'ApiException', 'webapi', 'webapi_class', 'install_api_list',
]

_api_list = []

class ApiException(Exception):
    def __init__(self, result = -1, message = 'Unknown error'):
        self._result = result
        self._message = message

    @property
    def result(self):
        return self._result

    @property
    def message(self):
        return self._message

class _ApiMethodWrapper(object):
    def __init__(self, req_cls, rsp_cls, callback,
                    desc = '',
                    exception_handler = None,
                    param_err_handler = None,
                    ):
        self._req_cls = req_cls
        self._rsp_cls = rsp_cls
        self._callback = callback
        self._desc = desc
        self._exception_handler = exception_handler
        self._param_err_handler = param_err_handler
        method_name = callback.func_name
        if method_name.endswith('_POST'):
            self._dataset = 'form'
            self._http_method = ['POST',]
            self._method_name = method_name[:-5]
        elif method_name.endswith('_GET'):
            self._dataset = 'args'
            self._http_method = ['GET',]
            self._method_name = method_name[:-4]
        else:
            self._dataset = 'values'
            self._http_method = ['GET', 'POST',]
            self._method_name = method_name

    @property
    def request_type(self):
        return self._req_cls

    @property
    def response_type(self):
        return self._rsp_cls

    @property
    def http_method(self):
        return self._http_method

    @property
    def method_name(self):
        return self._method_name

    @property
    def desc(self):
        return self._desc

    def __call__(self, obj):
        need_run = True
        rsp = self._rsp_cls()
        if self._req_cls is not None:
            req = self._req_cls()
            reqdata = getattr(request, self._dataset)
            for key, field_info in self._req_cls._get_fields():
                try:
                    if isinstance(field_info, FileField):
                        has_key = key in request.files
                    else:
                        has_key = key in reqdata
                    if not has_key:
                        if field_info.required:
                            logging.error('while calling %s, required field %s is missing',
                                        request.path, key)
                            raise Exception('')
                        continue
                    if field_info.repeated:
                        if isinstance(field_info, FileField):
                            setattr(req, key, request.files.getlist(key))
                        else:
                            setattr(req, key, reqdata.getlist(key))
                    else:
                        if isinstance(field_info, FileField):
                            setattr(req, key, request.files.get(key))
                        else:
                            setattr(req, key, reqdata.get(key))
                except Exception, ex:
                    traceback.print_exc()
                    if self._param_err_handler:
                        self._param_err_handler(key, req, rsp, ex)
                        need_run = False
                    else:
                        return ''
        else:
            req = None
        try:
            if need_run:
                ret = self._callback(obj, req, rsp)
        except ApiException, ex:
            if self._exception_handler:
                self._exception_handler(req, rsp, ex)
        return rsp.to_json(ensure_ascii = False, indent = 4)     

def webapi(req_cls, rsp_cls, desc = '', exception_handler = None, param_err_handler = None):
    def _inner(callback):
        inner = _ApiMethodWrapper(req_cls, rsp_cls, callback,
                    desc = desc,
                    exception_handler = exception_handler,
                    param_err_handler = param_err_handler,
                    )
        return functools.update_wrapper(inner, callback)
    return _inner

def webapi_class(app, **kwargs):
    def _inner(cls):
        global _api_list
        apis = inspect.getmembers(cls, lambda f: isinstance(f, _ApiMethodWrapper))
        for name, wrapper in apis:
            _api_list.append((app, cls, name, wrapper))
        return cls
    return _inner

def install_api_list(app, prefix):
    if prefix.endswith('/'):
        prefix = prefix[:-1]

    tpl_dir = osp.join(osp.dirname(osp.abspath(__file__)), '..', '..', 'templates', 'apilist')
    tpl_lookup = TemplateLookup(
        directories = [tpl_dir,],
        input_encoding = 'utf-8',
        output_encoding = 'utf-8',
    )

    static_dir = osp.abspath(
        osp.join(
            osp.dirname(osp.abspath(__file__)),
            '..',
            '..',
            'static',
            'devoops'
        )
    )
    apilist_mod = Blueprint(
        'apilist',
        __name__,
        static_folder = static_dir,
    )

    def _render_template(filename, **kwargs):
        tpl = tpl_lookup.get_template(filename)
        if not tpl:
            abort(503)
        common_params = dict(
            url_for=url_for,
            request=request,
            url_prefix = prefix,
        )
        common_params.update(kwargs)
        return tpl.render(**common_params)

    @apilist_mod.route('/')
    def api_list():
        return _render_template(
            'api_list.html',
            api_list = _api_list,
        )

    @apilist_mod.route('/<int:index>/debug')
    def api_debug(index):
        app, cls, method_name, wrapper = _api_list[index]
        url_route = app.name + '.' + cls.__name__ \
                if isinstance(app, Blueprint) else cls.__name__
        return _render_template(
            'api_debug.html',
            api_url = url_for(url_route, name = wrapper.method_name),
            app = app,
            cls = cls,
            method_name = wrapper.method_name,
            wrapper = wrapper
        )

    @apilist_mod.route('/<int:index>/doc')
    def api_doc(index):
        app, cls, method_name, wrapper = _api_list[index]
        url_route = app.name + '.' + cls.__name__ \
                if isinstance(app, Blueprint) else cls.__name__

        def _get_all_types(typ):
           types = [typ]
           for _, info in typ._get_fields():
               if isinstance(info, MessageField):
                   sub_types = _get_all_types(info.cls)
                   types += sub_types
           return types
        req_types = _get_all_types(wrapper.request_type)
        rsp_types = _get_all_types(wrapper.response_type)
        print rsp_types
        return _render_template(
            'api_doc.html',
            api_url = url_for(url_route, name = wrapper.method_name),
            app = app,
            cls = cls,
            method_name = wrapper.method_name,
            wrapper = wrapper,
            req_types = req_types,
            rsp_types = rsp_types,
        )

    app.register_blueprint(apilist_mod, url_prefix = prefix)



