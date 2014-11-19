import inspect
import fields

class Model(dict):

    obj_id = fields.ObjIdField(name = '_id')

    def __init__(self, data = None):
        if data is not None:
            super(Model, self).__init__(data)
        else:
            super(Model, self).__init__()

        cls_fields = self.__class__.get_fields()

    def data_ref(self):
        return dict(self)

    def data(self, skip_fields = ()):
        if not skip_fields:
            return self.copy()
        ret_data = self.copy()
        for field_name in skip_fields:
            del ret_data[field_name]
        return ret_data

    def getlist(self, key, default = []):
        return [self[key]] if key in self else default

    @classmethod
    def collection_name(cls):
        if hasattr(cls, '__collection__'):
            return cls.__collection__
        name = ''.join(['_' + x.lower() if x.isupper() else x for x in list(cls.__name__)])
        if '_' == name[0]:
            name = name[1:]
        cls.__collection__ = name
        return name

    @classmethod
    def get_fields(cls):
        if not hasattr(cls, '__fields__'):
            raw_fields = inspect.getmembers(
                            cls,
                            lambda value: isinstance(value, fields.BasicField),
                        )
            cls.__fields__ = []
            for field_name, field_info in raw_fields:
                field_info.field_name = field_name
                if field_info.name is None:
                    field_info.name = field_name
                cls.__fields__.append((field_name, field_info))
        return cls.__fields__

    @classmethod
    def from_bson_data(cls, data):
        cls_fields = cls.get_fields()
        model = cls()
        for field_name, field_info in cls_fields:
            if not field_info.name in data:
                continue
            model[field_name] = field_info.parse(data[field_info.name])
        return model

    @classmethod
    def to_bson_data(cls, model):
        cls_fields = cls.get_fields()
        data = {}
        for field_name, field_info in cls_fields:
            field_value = getattr(model, field_name)
            if field_value is not None:
                data[field_info.name] = field_info.serialize(field_value)
        return data

class FakeModel(dict):
    def data(self):
        return self
