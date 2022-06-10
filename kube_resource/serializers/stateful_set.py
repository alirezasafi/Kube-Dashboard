from rest_framework import serializers
from kubernetes import client
from .common import ObjectMeta
from .deployment import LabelSelector
from .pod import PodTemplateSpec
from .persistent_volume import PersistentVolumeClaim


class StatefulSetPersistentVolumeClaimRetentionPolicy(serializers.Serializer):
    when_deleted = serializers.CharField()
    when_scaled = serializers.CharField()

    class Meta:
        model = client.V1StatefulSetPersistentVolumeClaimRetentionPolicy


class RollingUpdateStatefulSetStrategy(serializers.Serializer):
    partition = serializers.IntegerField()

    class Meta:
        model = client.V1RollingUpdateStatefulSetStrategy


class StatefulSetUpdateStrategy(serializers.Serializer):
    rolling_update = RollingUpdateStatefulSetStrategy()
    type = serializers.CharField()

    class Meta:
        model = client.V1StatefulSetUpdateStrategy


class StatefulSetSpec(serializers.Serializer):
    min_ready_seconds = serializers.IntegerField()
    persistent_volume_claim_retention_policy = StatefulSetPersistentVolumeClaimRetentionPolicy()
    pod_management_policy = serializers.CharField()
    replicas = serializers.IntegerField()
    revision_history_limit = serializers.IntegerField()
    selector = LabelSelector()
    service_name = serializers.CharField()
    template = PodTemplateSpec()
    update_strategy = StatefulSetUpdateStrategy()
    volume_claim_templates = serializers.ListField(
        child=PersistentVolumeClaim()
    )

    class Meta:
        model = client.V1StatefulSetSpec


class StatefulSetCondition(serializers.Serializer):
    last_transition_time = serializers.DateTimeField()
    message = serializers.CharField()
    reason = serializers.CharField()
    status = serializers.CharField()
    type = serializers.CharField()

    class Meta:
        model = client.V1StatefulSetCondition


class StatefulSetStatus(serializers.Serializer):
    available_replicas = serializers.IntegerField()
    collision_count = serializers.IntegerField()
    conditions = serializers.ListField(
        child=StatefulSetCondition()
    )
    current_replicas = serializers.IntegerField()
    current_revision = serializers.IntegerField()
    observed_generation = serializers.IntegerField()
    ready_replicas = serializers.IntegerField()
    replicas = serializers.IntegerField()
    replicasupdate_revision = serializers.CharField()
    updated_replicas = serializers.IntegerField()

    class Meta:
        model = client.V1StatefulSetStatus


class StatefulSet(serializers.Serializer):
    api_version = serializers.CharField()
    kind = serializers.CharField()
    metadata = ObjectMeta()
    spec = StatefulSetSpec()
    status = StatefulSetStatus()

    class Meta:
        resource_object = "STATEFUL_SET"
        api_client = "apps_v1"
        model = client.V1StatefulSet
