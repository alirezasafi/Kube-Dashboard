from rest_framework import serializers
from kubernetes import client
from .common import ObjectMeta


class Secret(serializers.Serializer):
    metadata = ObjectMeta()
    data = serializers.DictField()
    type = serializers.CharField()
    string_data = serializers.DictField(write_only=True)

    class Meta:
        model = client.V1Secret
