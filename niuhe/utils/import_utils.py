#!-*- coding=utf-8 -*-

__all__ = ['load_contents', 'TypeFilter', 'InstaneFilter', 'import_types']

def load_contents(root_path, file_suffix, package, obj_filter, locals_dict, all_list, decorators = []):
    import os
    import os.path as osp
    import importlib
    import logging

    for src_file in os.listdir(root_path):
        if not src_file.endswith(file_suffix + '.py'):
            continue
        m = importlib.import_module(
            '.' + src_file[:-3],
            package = package,
        )
        for key in dir(m):
            obj = getattr(m, key)
            if obj_filter(obj):
                for decorator in decorators:
                    obj = decorator(obj)
                locals_dict[key] = obj
                all_list.append(key)
                logging.info('%s/%s:%s imported', root_path, src_file, key)


class TypeFilter(object):

    def __init__(self, type_):
        self._type = type_

    def __call__(self, obj):
        return isinstance(obj, type) and issubclass(obj, self._type) and obj != self._type


class InstanceFilter(object):

    def __init__(self, type_):
        self._type = type_

    def __call__(self, obj):
        return isinstance(obj, type_)

def import_types(file_suffix, target_type, decorators = []):
    import os
    import os.path as osp
    import inspect
    stack = inspect.stack()
    target_obj, caller_path = stack[1][0:2]
    if not '__all__' in target_obj.f_locals:
        target_obj.f_locals['__all__'] = []
    load_contents(
        root_path       = osp.dirname(caller_path),
        file_suffix     = file_suffix,
        package         = target_obj.f_locals['__package__'],
        obj_filter      = TypeFilter(target_type),
        locals_dict     = target_obj.f_locals,
        all_list        = target_obj.f_locals['__all__'],
        decorators      = decorators,
    )


