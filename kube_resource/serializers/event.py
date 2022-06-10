from rest_framework import serializers
from kubernetes import client
from kube_client.manager import Manager
from .common import ObjectMeta, ObjectReference


class EventSource(serializers.Serializer):
    component = serializers.CharField()
    host = serializers.CharField()

    class Meta:
        model = client.V1EventSource


class EventSeries(serializers.Serializer):
    count = serializers.IntegerField()
    last_observed_time = serializers.DateTimeField()

    class Meta:
        model = client.CoreV1EventSeries


class Event(serializers.Serializer, Manager):
    action = serializers.CharField()
    api_version = serializers.CharField()
    kind = serializers.CharField()
    count = serializers.IntegerField()
    event_time = serializers.DateTimeField()
    first_timestamp = serializers.DateTimeField()
    last_timestamp = serializers.DateTimeField()
    message = serializers.CharField()
    reason = serializers.CharField()
    reporting_component = serializers.CharField()
    reporting_instance = serializers.CharField()
    type = serializers.CharField()
    source = EventSource()
    series = EventSeries()
    related = ObjectReference()
    metadata = ObjectMeta()
    involved_object = ObjectReference()

    class Meta:
        resource_object = "EVENT"
        api_client = "core_v1"
        model = client.CoreV1Event
