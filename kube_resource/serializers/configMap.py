from rest_framework import serializers
from .common import ObjectMeta


class ConfigMap(serializers.Serializer):
    metadata = ObjectMeta()
    data = serializers.DictField()
