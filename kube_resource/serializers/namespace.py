from rest_framework import serializers
from kubernetes import client
from kube_client.manager import Manager
from .common import ObjectMeta


class NamespaceSpec(serializers.Serializer):
    finalizers = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        model = client.V1NamespaceSpec


class Namespace(serializers.Serializer, Manager):
    metadata = ObjectMeta()
    spec = NamespaceSpec()

    class Meta:
        resource_object = "NAMESPACE"
        api_client = "core_v1"
        model = client.V1Namespace
