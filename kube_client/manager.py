from collections import OrderedDict
from rest_framework.fields import set_value
from .client import KubeClient
from .config import Configuration


class Manager:
    _client = KubeClient()
    configuration: Configuration = NotImplementedError

    def get_resource_meta_data(self) -> (str, str):
        if not self.Meta.resource_object or not self.Meta.api_client:
            raise NotImplementedError(f"the resource_obj or api_client not defined in class: {self}")
        return self.Meta.resource_object, self.Meta.api_client

    def list(self, selectors={}, **kwargs):
        """
        get the list of resource of object.
        :param selectors:
        :param kwargs:
        :return:
        """
        kwargs = {**kwargs, **selectors}
        resource_obj, api_client = self.get_resource_meta_data()
        return self._client.list(resource_obj, api_client, self.configuration, **kwargs)

    def get(self, **kwargs):
        """
        get the resource object details
        :param kwargs:
        :return:
        """
        resource_obj, api_client = self.get_resource_meta_data()
        return self._client.get(resource_obj, api_client, self.configuration, **kwargs)

    def destroy(self, name, **kwargs):
        """
        delete the resource.
        :param name: name of the resource.
        :param kwargs: client kwargs data.
        :return:
        """
        resource_obj, api_client = self.get_resource_meta_data()
        client_kwargs = {
            "name": name,
            **kwargs
        }
        return self._client.delete(resource_obj, api_client, self.configuration, **client_kwargs)

    def patch(self, name, **kwargs):
        """
        update the resource.
        :param name: name of the resource.
        :param kwargs: client kwargs data.
        :return:
        """
        resource_obj, api_client = self.get_resource_meta_data()
        body = self.deserialize()
        return self._client.patch(name, body, resource_obj, api_client, self.configuration, **kwargs)

    def create_resource(self, **kwargs):
        """create the resource"""
        body = self.deserialize()
        resource_obj, api_client = self.get_resource_meta_data()
        return self._client.create(body, resource_obj, api_client, self.configuration, **kwargs)

    def deserialize(self):
        """
        convert json formatted data to resource object model.
        :return:
        """
        fields = self.fields.values()
        model = self.Meta.model
        data = self.validated_data
        return self.to_internal_model_value(data, fields, model)

    def serialize(self, data, many=False):
        """
        convert resource object model to json data
        :param data: the resource object model data
        :param many:
        :return:
        """
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
        if not data:
            return {}
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

    def to_internal_model_value(self, data, fields, model):
        model_args = {}
        for field in fields:
            if field.field_name not in data:
                continue
            if hasattr(field, 'child') and hasattr(field.child, 'Meta'):  # for list of resource model
                model_args[field.field_name] = []
                for element in data[field.field_name]:
                    model_args[field.field_name].append(
                        self.to_internal_model_value(
                            element, field.child.fields.values(), field.child.Meta.model
                        )
                    )
            elif hasattr(field, 'fields') and hasattr(field, 'Meta'):  # for nested resource models
                model_args[field.field_name] = self.to_internal_model_value(
                    data[field.field_name], field.fields.values(), field.Meta.model
                )
            else:
                model_args[field.field_name] = field.get_value(data)
        return model(**model_args)
