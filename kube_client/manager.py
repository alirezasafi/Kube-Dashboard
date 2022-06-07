from collections import OrderedDict
from rest_framework.fields import set_value, Field
from .client import KubeClient


class Manager:
    _client = KubeClient()

    def get_resource_meta_data(self) -> (str, str):
        if not self.Meta.resource_object or not self.Meta.api_client:
            raise NotImplementedError(f"the resource_obj or api_client not defined in class: {self}")
        return self.Meta.resource_object, self.Meta.api_client

    def list(self, configuration, namespace="default", selectors={}):
        """get the list of resource of object."""
        resource_obj, api_client = self.get_resource_meta_data()
        return self._client.list(namespace, selectors, resource_obj, api_client, configuration)

    def get(self, configuration, name, namespace="default"):
        """get the resource object details"""
        resource_obj, api_client = self.get_resource_meta_data()
        return self._client.get(namespace, name, resource_obj, api_client, configuration)

    def serialize(self, data, many=False):
        """serialize kube-client response to json data"""
        if not hasattr(self, "fields"):
            raise NotImplementedError("use proper serializer to serialize data")
        if many:
            response = []
            items = data.items
            for item in items:
                response.append(self.to_representation_data(item.to_dict(), self.fields.values()))
            return response
        else:
            return self.to_representation_data(data.to_dict(), self.fields.values())

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
