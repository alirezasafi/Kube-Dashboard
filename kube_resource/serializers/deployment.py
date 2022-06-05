from rest_framework import serializers
from kube_client.manager import Manager
from .pod import PodTemplateSpec
from .common import ObjectMeta


class LabelSelector(serializers.Serializer):
    match_labels = serializers.DictField()


class RollingUpdateDeployment(serializers.Serializer):
    max_unavailable = serializers.IntegerField()
    max_surge = serializers.IntegerField()


class DeploymentStrategy(serializers.Serializer):
    type = serializers.CharField(default="RollingUpdate")
    rolling_update = RollingUpdateDeployment()


class DeploymentSpec(serializers.Serializer):
    replicas = serializers.IntegerField(default=1)
    selector = LabelSelector()
    template = PodTemplateSpec()
    strategy = DeploymentStrategy()
    min_ready_seconds = serializers.IntegerField()
    revision_history_limit = serializers.IntegerField()
    paused = serializers.CharField()


class DeploymentStatus(serializers.Serializer):
    observed_generation = serializers.IntegerField()
    replicas = serializers.IntegerField()
    updated_replicas = serializers.IntegerField()
    available_replicas = serializers.IntegerField()
    unavailable_replicas = serializers.IntegerField()


class Deployment(serializers.Serializer, Manager):
    metadata = ObjectMeta()
    spec = DeploymentSpec()
    status = DeploymentStatus()

    class Meta:
        resource_object = "DEPLOYMENT"
