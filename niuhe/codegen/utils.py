#!/usr/bin/env python
#!-*- coding=utf-8 -*-

import os
import os.path as osp

def mkdir_p(*paths):
    fullpath = osp.join(*paths)
    if not osp.isdir(fullpath):
        os.mkdir(fullpath)
    
def mkdir_rp(*paths):
    for l in xrange(0, len(paths)):
        mkdir_p(*paths[:l + 1])

def copy_dir(from_path, to_path):
    from_path = osp.abspath(from_path)
    if not osp.isdir(from_path):
        print '%s is not dir. skipped' % from_path
        return
    to_path = osp.abspath(to_path)
    if not osp.isdir(to_path):
        mkdir_p(to_path)

    for root, dirnames, filenames in os.walk(from_path):
        root = osp.abspath(root)
        suffix = root[len(from_path) + 1:]
        target_root = osp.join(to_path, suffix)
        
        for dirname in dirnames:
            mkdir_p(osp.join(target_root, dirname))

        for filename in filenames:
            from_file_path = osp.join(root, filename)
            to_file_path = osp.join(target_root, filename)
            with file(from_file_path) as from_file:
                with file(to_file_path, 'w') as to_file:
                    to_file.write(from_file.read())
        

