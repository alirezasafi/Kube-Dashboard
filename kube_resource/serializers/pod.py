from rest_framework import serializers
from kubernetes import client
from kube_client.manager import Manager
from .common import ObjectMeta, LocalObjectReference


class ContainerPort(serializers.Serializer):
    name = serializers.CharField()
    host_port = serializers.IntegerField()
    container_port = serializers.IntegerField()
    protocol = serializers.CharField(default="TCP")

    class Meta:
        model = client.V1ContainerPort


class ObjectFileSelector(serializers.Serializer):
    api_version = serializers.CharField()
    field_path = serializers.CharField(required=True)

    class Meta:
        model = client.V1ObjectFieldSelector


class ResourceFieldSelector(serializers.Serializer):
    container_name = serializers.CharField()
    resource = serializers.CharField(required=True)
    divisor = serializers.CharField()

    class Meta:
        model = client.V1ResourceFieldSelector


class ConfigMapKeySelector(serializers.Serializer):
    name = serializers.CharField()
    key = serializers.CharField(required=True)

    class Meta:
        model = client.V1ConfigMapKeySelector


class SecretKeySelector(serializers.Serializer):
    name = serializers.CharField()
    key = serializers.CharField(required=True)

    class Meta:
        model = client.V1SecretKeySelector


class EnvVarSource(serializers.Serializer):
    field_ref = ObjectFileSelector()
    resource_field_ref = ResourceFieldSelector()
    config_map_key_ref = ConfigMapKeySelector()
    secret_key_ref = SecretKeySelector()

    class Meta:
        model = client.V1EnvVarSource


class SecretEnvSource(serializers.Serializer):
    name = serializers.CharField()
    optional = serializers.BooleanField()

    class Meta:
        model = client.V1SecretEnvSource


class ConfigMapEnvSource(serializers.Serializer):
    name = serializers.CharField()
    optional = serializers.BooleanField()

    class Meta:
        model = client.V1ConfigMapEnvSource


class EnvFromSource(serializers.Serializer):
    config_map_ref = ConfigMapEnvSource()
    secret_ref = SecretEnvSource()

    class Meta:
        model = client.V1EnvFromSource


class EnvVar(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()
    value_from = EnvVarSource()

    class Meta:
        model = client.V1EnvVar


class ResourceRequirements(serializers.Serializer):
    limits = serializers.DictField()
    requests = serializers.DictField()

    class Meta:
        model = client.V1ResourceRequirements


class VolumeMount(serializers.Serializer):
    name = serializers.CharField()
    read_only = serializers.BooleanField()
    mount_path = serializers.CharField()

    class Meta:
        model = client.V1VolumeMount


class HTTPHeader(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()

    class Meta:
        model = client.V1HTTPHeader


class HTTPGetAction(serializers.Serializer):
    path = serializers.CharField()
    port = serializers.IntegerField()
    scheme = serializers.CharField(default="HTTP")
    http_headers = serializers.ListField(
        child=HTTPHeader()
    )

    class Meta:
        model = client.V1HTTPGetAction


class TCPSocketAction(serializers.Serializer):
    port = serializers.IntegerField()

    class Meta:
        model = client.V1TCPSocketAction


class ExecAction(serializers.Serializer):
    command = serializers.CharField()

    class Meta:
        model = client.V1ExecAction


class Probe(serializers.Serializer):
    http_get = HTTPGetAction()
    tcp_socket = TCPSocketAction()
    exec = ExecAction()
    initial_delay_seconds = serializers.IntegerField(default=5)
    timeout_seconds = serializers.IntegerField()
    success_threshold = serializers.IntegerField()
    failure_threshold = serializers.IntegerField()
    period_seconds = serializers.IntegerField()

    class Meta:
        model = client.V1Probe


class Handler(serializers.Serializer):
    http_get = HTTPGetAction()
    tcp_socket = TCPSocketAction()
    exec = ExecAction()

    class Meta:
        model = client.V1LifecycleHandler


class Lifecycle(serializers.Serializer):
    post_start = Handler()
    pre_Stop = Handler()

    class Meta:
        model = client.V1Lifecycle


class Container(serializers.Serializer):
    name = serializers.CharField()
    image = serializers.CharField()
    ports = serializers.ListField(
        child=ContainerPort()
    )
    env = serializers.ListField(
        child=EnvVar()
    )
    env_from = serializers.ListField(
        child=EnvFromSource()
    )
    resources = ResourceRequirements()
    volume_mounts = serializers.ListField(
        child=VolumeMount()
    )
    lifecycle = Lifecycle()
    liveness_probe = Probe()
    readiness_probe = Probe()
    image_pull_policy = serializers.CharField(default="IfNotPresent")
    command = serializers.ListField(
        child=serializers.CharField()
    )
    args = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        model = client.V1Container


class SecretVolumeSource(serializers.Serializer):
    secret_name = serializers.CharField()
    optional = serializers.BooleanField()
    default_mode = serializers.IntegerField()

    class Meta:
        model = client.V1SecretVolumeSource


class KeyToPath(serializers.Serializer):
    key = serializers.CharField(required=True)
    path = serializers.CharField(required=True)

    class Meta:
        model = client.V1KeyToPath


class ConfigMapVolumeSource(serializers.Serializer):
    name = serializers.CharField()
    optional = serializers.BooleanField()
    default_mode = serializers.IntegerField()

    class Meta:
        model = client.V1ConfigMapVolumeSource


class EmptyDirVolumeSource(serializers.Serializer):
    medium = serializers.CharField()

    class Meta:
        model = client.V1EmptyDirVolumeSource


class NFSVolumeSource(serializers.Serializer):
    path = serializers.CharField()
    read_only = serializers.BooleanField()
    server = serializers.CharField()

    class Meta:
        model = client.V1NFSVolumeSource


class HostPathVolumeSource(serializers.Serializer):
    path = serializers.CharField()

    class Meta:
        model = client.V1HostPathVolumeSource


class GCPersistentDiskVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    partition = serializers.IntegerField()
    pd_name = serializers.CharField()
    readOnly = serializers.BooleanField()

    class Meta:
        model = client.V1GCEPersistentDiskVolumeSource


class AWSElasticBlockStoreVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    partition = serializers.IntegerField()
    read_only = serializers.BooleanField()
    volume_id = serializers.CharField()

    class Meta:
        model = client.V1AWSElasticBlockStoreVolumeSource


class Volume(serializers.Serializer):
    name = serializers.CharField()
    aws_elastic_block_store = AWSElasticBlockStoreVolumeSource()
    config_map = ConfigMapVolumeSource()
    empty_dir = EmptyDirVolumeSource()
    gcp_persistent_disk = GCPersistentDiskVolumeSource()
    host_path = HostPathVolumeSource()
    nfs = NFSVolumeSource()
    secret = SecretVolumeSource()

    class Meta:
        model = client.V1Volume


class PodSpec(serializers.Serializer):
    volume = serializers.ListField(
        child=Volume()
    )
    containers = serializers.ListField(
        child=Container()
    )
    restart_policy = serializers.CharField(default="Always")
    termination_grace_periodSeconds = serializers.IntegerField()
    active_deadline_seconds = serializers.IntegerField()
    dns_policy = serializers.CharField(default="ClusterFirst")
    node_name = serializers.CharField()
    node_selector = serializers.DictField()
    selector = serializers.DictField()
    service_account_name = serializers.CharField(default="default")
    automount_service_account_token = serializers.BooleanField()
    image_pull_secrets = serializers.ListField(
        child=LocalObjectReference()
    )
    init_containers = serializers.ListField(
        child=Container()
    )

    class Meta:
        model = client.V1PodSpec


class PodTemplateSpec(serializers.Serializer):
    metadata = ObjectMeta()
    spec = PodSpec()

    class Meta:
        model = client.V1PodTemplateSpec


class Pod(serializers.Serializer, Manager):
    metadata = ObjectMeta()
    spec = PodSpec()

    class Meta:
        resource_object = "POD"
        api_client = "core_v1"
        model = client.V1Pod
