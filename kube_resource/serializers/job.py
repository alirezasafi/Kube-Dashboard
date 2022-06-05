from rest_framework import serializers
from .pod import PodTemplateSpec
from .common import ObjectMeta


class LabelSelector(serializers.Serializer):
    match_labels = serializers.DictField()


class JobSpec(serializers.Serializer):
    template = PodTemplateSpec()
    backoff_limit = serializers.IntegerField()
    active_deadline_seconds = serializers.IntegerField()
    completions = serializers.IntegerField()
    manual_selector = serializers.BooleanField()
    parallelism = serializers.IntegerField()
    selector = LabelSelector()


class JobTemplateSpec(serializers.Serializer):
    metadata = ObjectMeta()
    spec = JobSpec()


class Job(serializers.Serializer):
    metadata = ObjectMeta()
    spec = JobSpec()
