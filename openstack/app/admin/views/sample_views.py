#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import logging
from flask import request, abort
from niuhe.views.dispatch_view import DispatchView, install_to

from .. import render_template

from ..forms import SampleForm
from app._common.models import *

from . import AdminDispatchView

print AdminDispatchView
class Sample(AdminDispatchView):
    __title__       = '例子'
    __model_type__  = SampleModel
    __form_type__   = SampleForm


class TestFirst(AdminDispatchView):
	__title__       = '测试1'
	__model_type__  = SampleModel
	__form_type__   = SampleForm


class TestSecond(AdminDispatchView):
	__title__       = '测试2'
	__model_type__  = SampleModel
	__form_type__   = SampleForm
	__skipfields__  = ['name']

class Test(AdminDispatchView):

	list_template = "/test.html"

	def _render(self, tpl_name, **kwargs):
		tpl_kwargs = {}
		tpl_kwargs.update(kwargs)
		return render_template(tpl_name, **tpl_kwargs)
	
	def list_GET(self):
		if not self._allow_list():
			abort(403)
			
		return self._render(
			self.list_template,
			title = '测试',
			test = 'python',
			skip_fields = ['name'],
			)
class Dashboard(AdminDispatchView):
	list_template = "/dashboard.html"
	def _render(self, tpl_name, **kwargs):
		tpl_kwargs = {}
		tpl_kwargs.update(kwargs)
		return render_template(tpl_name, **tpl_kwargs)

	def list_GET(self):
		if not self._allow_list():
			abort(403)

		return self._render(
			self.list_template,
			title = '橄榄',
			)