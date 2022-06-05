from rest_framework import serializers
from .common import ObjectMeta


class NamespaceSpec(serializers.Serializer):
    finalizers = serializers.ListField(
        child=serializers.CharField()
    )


class Namespace(serializers.Serializer):
    metadata = ObjectMeta()
    spec = NamespaceSpec()
