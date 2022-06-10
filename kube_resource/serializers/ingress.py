from rest_framework import serializers
from kubernetes import client
from .common import ObjectMeta


class IngressBackend(serializers.Serializer):
    service_name = serializers.CharField()
    service_port = serializers.CharField()

    class Meta:
        model = client.V1IngressBackend


class HTTPIngressPath(serializers.Serializer):
    path = serializers.CharField()
    backend = IngressBackend()

    class Meta:
        model = client.V1HTTPIngressPath


class HTTPIngressRuleValue(serializers.Serializer):
    paths = serializers.ListField(
        child=HTTPIngressPath()
    )

    class Meta:
        model = client.V1HTTPIngressRuleValue


class IngressRule(serializers.Serializer):
    host = serializers.CharField()
    http = HTTPIngressRuleValue()

    class Meta:
        model = client.V1IngressRule


class IngresTLS(serializers.Serializer):
    hosts = serializers.ListField(
        child=serializers.CharField()
    )
    secret_name = serializers.CharField()

    class Meta:
        model = client.V1IngressTLS


class IngressSpec(serializers.Serializer):
    backend = IngressBackend()
    rules = serializers.ListField(
        child=IngressRule()
    )
    tls = serializers.ListField(
        child=IngresTLS()
    )

    class Meta:
        model = client.V1IngressSpec


class Ingress(serializers.Serializer):
    metadata = ObjectMeta()
    spec = IngressSpec()

    class Meta:
        model = client.V1Ingress
