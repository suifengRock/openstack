#!/usr/bin/env python
#!-*- coding=utf-8 -*-

# define your model(s) like this:

from app import db

class SampleModel(db.Model):
    __tablename__   = 't_sample'
    __table_args__  = (
        db.Index('index1', 'title'),
    )

    sn          = db.Column(db.String(10), primary_key=True)
    category    = db.Column(db.Integer, index=True)
    title       = db.Column(db.String(128))

