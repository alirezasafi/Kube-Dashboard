from rest_framework import serializers
from .common import ObjectMeta


class ServicePort(serializers.Serializer):
    name = serializers.CharField()
    protocol = serializers.CharField(default="TCP")
    port = serializers.IntegerField()
    target_port = serializers.CharField()
    node_port = serializers.IntegerField()


class ServiceSpec(serializers.Serializer):
    ports = serializers.ListField(
        child=ServicePort()
    )
    selector = serializers.DictField()
    cluster_ip = serializers.CharField(help_text="once field")
    loadBalancer_ip = serializers.CharField(help_text="once field")
    type = serializers.CharField(default="ClusterIP")
    session_affinity = serializers.CharField(default="None")
    loadB_balancer_source_ranges = serializers.ListField(
        child=serializers.CharField()
    )


class Service(serializers.Serializer):
    metadata = ObjectMeta()
    spec = ServiceSpec()
