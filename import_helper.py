#!-*- coding=utf-8 -*-

__all__ = ['load_contents', 'TypeFilter']

def load_contents(root_path, file_surfix, package, obj_filter, locals_dict, all_list):
    import os
    import os.path as osp
    import importlib

    for src_file in os.listdir(root_path):
        if not src_file.endswith(file_surfix + '.py'):
            continue
        m = importlib.import_module(
            '.' + src_file[:-3],
            package = package,
        )
        for key in dir(m):
            obj = getattr(m, key)
            if obj_filter(obj):
                locals_dict[key] = obj
                all_list.append(key)


class TypeFilter(object):
    def __init__(self, type_):
        self._type = type_
    def __call__(self, obj):
        return isinstance(obj, type) and issubclass(obj, self._type)
