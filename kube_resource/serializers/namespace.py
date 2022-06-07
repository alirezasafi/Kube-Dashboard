from rest_framework import serializers
from kube_client.manager import Manager
from .common import ObjectMeta


class NamespaceSpec(serializers.Serializer):
    finalizers = serializers.ListField(
        child=serializers.CharField()
    )


class Namespace(serializers.Serializer, Manager):
    metadata = ObjectMeta()
    spec = NamespaceSpec()

    class Meta:
        resource_object = "NAMESPACE"
        api_client = "core_v1"
