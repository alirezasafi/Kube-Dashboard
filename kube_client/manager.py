from collections import OrderedDict
from rest_framework.fields import set_value, Field
from .client import KubeClient


class Manager:
    _client = KubeClient()

    def list(self, configuration, namespace="default"):
        """get the list of resource of object."""
        if not self.Meta.resource_object:
            raise NotImplementedError(f"the resource obj attr not defined in class: {self}")
        resource_obj = self.Meta.resource_object
        return self._client.list(namespace, resource_obj, configuration)

    def serialize(self, data, many=False):
        """serialize kube-client response to json data"""
        items = data.items
        response = []
        if many:
            if not hasattr(self, "fields"):
                raise NotImplementedError("use proper serializer to serialize data")
            for item in items:
                response.append(self.to_representation_data(item.to_dict(), self.fields.values()))
            return response
        else:
            return self.to_representation_data(data.items, self.fields.values())

    def to_representation_data(self, data, fields):
        """use serializer field to get the proper value"""
        ret = OrderedDict()
        for field in fields:
            if field.field_name not in data:
                continue
            if hasattr(field, 'fields'):
                set_value(
                    ret,
                    [field.field_name],
                    self.to_representation_data(data[field.field_name], field.fields.values())
                )
            else:
                primitive_value = field.get_value(data)
                set_value(ret, field.source_attrs, primitive_value)
        return ret
