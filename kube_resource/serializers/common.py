from rest_framework import serializers


class OwnerReference(serializers.Serializer):
    api_version = serializers.CharField()
    block_owner_deletion = serializers.BooleanField()
    controller = serializers.BooleanField()
    kind = serializers.CharField()
    name = serializers.CharField()
    uid = serializers.CharField()


class ObjectMeta(serializers.Serializer):
    annotations = serializers.DictField(allow_null=True)
    creation_timestamp = serializers.DateTimeField(read_only=True)
    deletion_grace_period_seconds = serializers.IntegerField(read_only=True)
    finalizers = serializers.ListField(
        child=serializers.CharField()
    )
    generate_name = serializers.CharField()
    generation = serializers.IntegerField(read_only=True)
    labels = serializers.DictField()
    name = serializers.CharField()
    namespace = serializers.CharField(default="default")
    owner_references = serializers.ListField(
        child=OwnerReference()
    )
    resource_version = serializers.CharField(read_only=True)
    self_link = serializers.CharField(read_only=True)
    uid = serializers.UUIDField(read_only=True,)


class TypedLocalObjectReference(serializers.Serializer):
    api_group = serializers.CharField()
    kind = serializers.CharField()
    name = serializers.CharField()


class ObjectReference(serializers.Serializer):
    api_version = serializers.CharField()
    field_path = serializers.CharField()
    kind = serializers.CharField()
    name = serializers.CharField()
    namespace = serializers.CharField()
    resource_version = serializers.CharField()
    uid = serializers.UUIDField()


class Preconditions(serializers.Serializer):
    resource_version = serializers.CharField()
    uid = serializers.UUIDField()


class DeleteOptions(serializers.Serializer):
    api_version = serializers.CharField()
    dry_run = serializers.ListField(
        child=serializers.CharField()
    )
    grace_period_seconds = serializers.IntegerField()
    kind = serializers.CharField()
    preconditions = Preconditions()
    propagation_policy = serializers.CharField()


class LocalObjectReference(serializers.Serializer):
    name = serializers.CharField()
