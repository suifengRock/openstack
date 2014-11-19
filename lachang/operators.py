class Condition(object):
    EQ = '='
    NE = '$ne'
    LT = '$lt'
    GT = '$gt'
    LTE = '$lte'
    GTE = '$gte'
    IN = '$in'
    NOT_IN = '$nin'
    REGEX = '$regex'

    def to_dict(self):
        raise NotImplemented()

class SingleCondition(Condition):

    def __init__(self, subj, op, obj):
        self._subj  = subj
        self._op    = op
        self._obj   = obj

    def to_dict(self, filter_dict):
        sub_name = self._subj.name
        if isinstance(self._obj, Condition):
            obj_value = {}
            self._obj.to_dict(obj_value)
        else:
            if isinstance(self._obj, (list, tuple)):
                obj_value = [self._subj.serialize(item) for item in self._obj]
            else:
                obj_value = self._subj.serialize(self._obj)
        if Condition.EQ == self._op:
            filter_dict[sub_name] = obj_value
        else:
            cond = filter_dict.get(sub_name, {})
            cond[self._op] = obj_value
            filter_dict[sub_name] = cond
        
        
class And(Condition):
    def __init__(self, *conditions):
        self._conditions = conditions

    def to_dict(self, filter_dict):
        for cond in self._conditions:
            cond.to_dict(filter_dict)

class Or(Condition):
    def __init__(self, *conditions):
        self._conditions = conditions

    def to_dict(self, filter_dict):
        conds = []
        for cond in self._conditions:
            item = {}
            cond.to_dict(item)
            conds.append(item)
        filter_dict['$or'] = conds 

class UpdateOp(object):
    SET = '$set'
    UNSET = '$unset'
    INC = '$inc'
    DEC = '$dec'

    def __init__(self, field, op, value):
        self._field = field
        self._op = op
        self._value = value

    def to_dict(self, op_dict):
        orig = op_dict.get(self._op, {})
        orig[self._field.name] = self._value
        op_dict[self._op] = orig

