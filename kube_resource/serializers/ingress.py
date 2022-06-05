from rest_framework import serializers
from .common import ObjectMeta


class IngressBackend(serializers.Serializer):
    service_name = serializers.CharField()
    service_port = serializers.CharField()


class HTTPIngressPath(serializers.Serializer):
    path = serializers.CharField()
    backend = IngressBackend()


class HTTPIngressRuleValue(serializers.Serializer):
    paths = serializers.ListField(
        child=HTTPIngressPath()
    )


class IngressRule(serializers.Serializer):
    host = serializers.CharField()
    http = HTTPIngressRuleValue()


class IngresTLS(serializers.Serializer):
    hosts = serializers.ListField(
        child=serializers.CharField()
    )
    secret_name = serializers.CharField()


class IngressSpec(serializers.Serializer):
    backend = IngressBackend()
    rules = serializers.ListField(
        child=IngressRule()
    )
    tls = serializers.ListField(
        child=IngresTLS()
    )


class Ingress(serializers.Serializer):
    metadata = ObjectMeta()
    spec = IngressSpec()
