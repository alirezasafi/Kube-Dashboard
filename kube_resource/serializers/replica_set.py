from rest_framework import serializers
from kubernetes import client
from .common import ObjectMeta
from .deployment import LabelSelector
from .pod import PodTemplateSpec


class ReplicaSetCondition(serializers.Serializer):
    last_transition_time = serializers.DateTimeField()
    message = serializers.CharField()
    reason = serializers.CharField()
    status = serializers.CharField()
    type = serializers.CharField()

    class Meta:
        model = client.V1ReplicaSetCondition


class ReplicaSetSpec(serializers.Serializer):
    min_ready_seconds = serializers.IntegerField()
    replicas = serializers.IntegerField()
    selector = LabelSelector()
    template = PodTemplateSpec()

    class Meta:
        model = client.V1ReplicaSetSpec


class ReplicaSetStatus(serializers.Serializer):
    available_replicas = serializers.IntegerField()
    conditions = serializers.ListField(
        child=ReplicaSetCondition()
    )
    fully_labeled_replicas = serializers.IntegerField()
    observed_generation = serializers.IntegerField()
    ready_replicas = serializers.IntegerField()
    replicas = serializers.IntegerField()

    class Meta:
        model = client.V1ReplicaSetStatus


class ReplicaSet(serializers.Serializer):
    api_version = serializers.CharField()
    kind = serializers.CharField()
    metadata = ObjectMeta()
    spec = ReplicaSetSpec()
    status = ReplicaSetStatus()

    class Meta:
        resource_object = "REPLICA_SET"
        api_client = "apps_v1"
        model = client.V1ReplicaSet
