from rest_framework import serializers
from kubernetes import client
from .common import ObjectMeta


class ConfigMap(serializers.Serializer):
    metadata = ObjectMeta()
    data = serializers.DictField()

    class Meta:
        model = client.V1ConfigMap
