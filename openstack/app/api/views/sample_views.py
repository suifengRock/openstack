#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import logging
import traceback
from flask import request
from niuhe.views.dispatch_view import DispatchView
from niuhe.views.webapi import webapi

from ..models import *
from ..services import *
from ..protos import *


class SampleEcho(DispatchView):

    @webapi(SimpleEchoReq, EchoRsp, desc = '这是一个简单的Echo接口')
    def simple_echo_GET(self, req, rsp):
        rsp.result = 0
        rsp.data = EchoRsp.data.new()
        rsp.data.content = req.content

    @webapi(NextEchoReq, EchoRsp, desc = '这是一个没那么简单的Echo接口')
    def next_echo(self, req, rsp):
        rsp.result = 10086
        rsp.message = 'test'
        rsp.data = EchoRsp.data.new()
        rsp.data.content = '#'.join(req.content_items)
