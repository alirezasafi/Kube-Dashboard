from rest_framework import serializers
from kubernetes import client
from .job import JobTemplateSpec
from .common import ObjectMeta, ObjectReference


class CronJobSpec(serializers.Serializer):
    concurrency_policy = serializers.CharField()
    failed_jobs_history_limit = serializers.IntegerField()
    job_template = JobTemplateSpec()
    schedule = serializers.CharField()
    starting_deadline_seconds = serializers.IntegerField()
    successful_job_history_limit = serializers.IntegerField()
    suspend = serializers.BooleanField()

    class Meta:
        model = client.V1CronJobSpec


class CronJobStatus(serializers.Serializer):
    active = serializers.ListField(
        child=ObjectReference()
    )
    last_schedule_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = client.V1CronJobStatus


class CronJob(serializers.Serializer):
    metadata = ObjectMeta()
    spec = CronJobSpec()
    status = CronJobStatus()

    class Meta:
        model = client.V1CronJob
