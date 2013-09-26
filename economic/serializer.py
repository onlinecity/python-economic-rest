from economic.utils import convert_from_camelCase


class EconomicSerializer(object):
    def __init__(self, auth, object_dict):
        self._mutable_fields = {}
        self._immutable_fields = {}
        self._field_translator = {}
        for field, value in object_dict.items():
            self._field_translator[convert_from_camelCase(field)] = field
            if field in ['self', 'customer']:
                self._immutable_fields[field] = value
            else:
                self._mutable_fields[field] = value

    def __repr__(self):
        return u"<%s: %s>" % (self.__class__.__name__, self.id)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._mutable_fields == other._mutable_fields and \
            self._immutable_fields == other._immutable_fields

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getattr__(self, item):
        if item not in ['_mutable_fields', '_immutable_fields', '_field_translator']:
            key = self._field_translator[item]
            if key in self._mutable_fields:
                return self._mutable_fields[key]
            elif key in self._immutable_fields[key]:
                return self._immutable_fields[key]
        super(EconomicSerializer, self).__getattribute__(item)

    def __setattr__(self, item, value):
        if item not in ['_mutable_fields', '_immutable_fields', '_field_translator']:
            key = self._field_translator[item]
            if key in self._mutable_fields:
                self._mutable_fields[key] = value
            elif key in self._immutable_fields:
                raise Exception("You can't change immutable fields")
        else:
            super(EconomicSerializer, self).__setattr__(item, value)