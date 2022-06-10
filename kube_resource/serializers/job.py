from rest_framework import serializers
from kubernetes import client
from .pod import PodTemplateSpec
from .common import ObjectMeta


class LabelSelector(serializers.Serializer):
    match_labels = serializers.DictField()

    class Meta:
        model = client.V1LabelSelector


class JobSpec(serializers.Serializer):
    template = PodTemplateSpec()
    backoff_limit = serializers.IntegerField()
    active_deadline_seconds = serializers.IntegerField()
    completions = serializers.IntegerField()
    manual_selector = serializers.BooleanField()
    parallelism = serializers.IntegerField()
    selector = LabelSelector()

    class Meta:
        model = client.V1JobSpec


class JobTemplateSpec(serializers.Serializer):
    metadata = ObjectMeta()
    spec = JobSpec()

    class Meta:
        model = client.V1JobTemplateSpec


class Job(serializers.Serializer):
    metadata = ObjectMeta()
    spec = JobSpec()

    class Meta:
        model = client.V1Job
