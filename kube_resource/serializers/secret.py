from rest_framework import serializers
from .common import ObjectMeta


class Secret(serializers.Serializer):
    metadata = ObjectMeta()
    data = serializers.DictField()
    type = serializers.CharField()
    string_data = serializers.DictField(write_only=True)
