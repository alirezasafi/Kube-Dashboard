from rest_framework import serializers
from kubernetes import client
from .common import ObjectMeta, ObjectReference
from .pod import NFSVolumeSource



class AWSElasticBlockStoreVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    partition = serializers.IntegerField()
    read_only = serializers.BooleanField()
    volume_id = serializers.IntegerField()

    class Meta:
        model = client.V1AWSElasticBlockStoreVolumeSource



class AzureDiskVolumeSource(serializers.Serializer):
    caching_mode = serializers.CharField()
    disk_name = serializers.CharField()
    disk_uri = serializers.CharField()
    fs_type = serializers.CharField()
    kind = serializers.CharField()
    read_only = serializers.BooleanField()
    class Meta:
        model = client.V1AzureDiskVolumeSource



class AzureFilePersistentVolumeSource(serializers.Serializer):
    read_only = serializers.BooleanField()
    secret_name = serializers.CharField()
    secret_namespace = serializers.CharField()
    share_name = serializers.CharField()

    class Meta:
        model = client.V1AzureFilePersistentVolumeSource

class SecretReference(serializers.Serializer):
    name = serializers.CharField()
    namespace = serializers.CharField()
    class Meta:
        model = client.V1SecretReference


class CephFSPersistentVolumeSource(serializers.Serializer):
    monitors = serializers.ListField(
        child=serializers.CharField()
    )
    path = serializers.CharField()
    read_only = serializers.BooleanField()
    secret_file = serializers.CharField()
    secret_ref = SecretReference()
    user = serializers.CharField()
    class Meta:
        model = client.V1CephFSPersistentVolumeSource


class CinderPersistentVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    read_only = serializers.BooleanField()
    secret_ref = SecretReference()
    volume_id = serializers.IntegerField()

    class Meta:
        model = client.V1CinderPersistentVolumeSource


class CSIPersistentVolumeSource(serializers.Serializer):
    controller_expand_secret_ref = SecretReference()
    controller_publish_secret_ref = SecretReference()
    driver = serializers.CharField()
    fs_type = serializers.CharField()
    node_publish_secret_ref = SecretReference()
    node_stage_secret_ref = SecretReference()
    read_only = serializers.BooleanField()
    volume_attributes = serializers.DictField()
    volume_handle = serializers.CharField()

    class Meta:
        model = client.V1CSIPersistentVolumeSource


class FCVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    lun = serializers.IntegerField()
    read_only = serializers.BooleanField()
    target_ww_ns = serializers.ListField(
        child=serializers.CharField()
    )
    wwids = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        model = client.V1FCVolumeSource


class FlexPersistentVolumeSource(serializers.Serializer):
    driver = serializers.CharField()
    fs_type = serializers.CharField()
    options = serializers.DictField()
    read_only = serializers.BooleanField()
    secret_ref = SecretReference()

    class Meta:
        model = client.V1FlexPersistentVolumeSource


class FlockerVolumeSource(serializers.Serializer):
    dataset_name = serializers.CharField()
    dataset_uuid = serializers.CharField()

    class Meta:
        model = client.V1FlockerVolumeSource


class GCEPersistentDiskVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    partition = serializers.IntegerField()
    pd_name = serializers.CharField()
    read_only = serializers.CharField()

    class Meta:
        model = client.V1GCEPersistentDiskVolumeSource


class GlusterfsPersistentVolumeSource(serializers.Serializer):
    endpoints = serializers.CharField()
    endpoints_namespace = serializers.CharField()
    path = serializers.CharField()
    read_only = serializers.BooleanField()

    class Meta:
        model = client.V1GlusterfsPersistentVolumeSource


class HostPathVolumeSource(serializers.Serializer):
    path = serializers.CharField()
    type = serializers.CharField()

    class Meta:
        model = client.V1HostPathVolumeSource


class ISCSIPersistentVolumeSource(serializers.Serializer):
    chap_auth_discovery = serializers.BooleanField()
    chap_auth_session = serializers.BooleanField()
    fs_type = serializers.CharField()
    initiator_name = serializers.CharField()
    iqn = serializers.CharField()
    iscsi_interface = serializers.CharField()
    lun = serializers.IntegerField()
    portals = serializers.ListField(
        child=serializers.CharField()
    )
    read_only = serializers.CharField()
    secret_ref = SecretReference()
    target_portal = serializers.CharField()


    class Meta:
        model = client.V1ISCSIPersistentVolumeSource


class LocalVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    path = serializers.CharField()

    class Meta:
        model = client.V1LocalVolumeSource


class NodeSelectorRequirement(serializers.Serializer):
    key = serializers.CharField()
    operator = serializers.CharField()
    values = serializers.ListField(
        child=serializers.CharField()
    )
    class Meta:
        model = client.V1NodeSelectorRequirement


class NodeSelectorTerm(serializers.Serializer):
    match_expressions = serializers.ListField(
        child=NodeSelectorRequirement()
    )
    match_fields = serializers.ListField(
        child=NodeSelectorRequirement()
    )
    class Meta:
        model = client.V1NodeSelectorTerm


class NodeSelector(serializers.Serializer):
    node_selector_terms = serializers.ListField(
        child=NodeSelectorTerm()
    )
    class Meta:
        model = client.V1NodeSelector


class VolumeNodeAffinity(serializers.Serializer):
    required = NodeSelector()
    class Meta:
        model = client.V1VolumeNodeAffinity


class PhotonPersistentDiskVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    pd_id = serializers.CharField()

    class Meta:
        model = client.V1PhotonPersistentDiskVolumeSource


class PortworxVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    read_only = serializers.BooleanField()
    volume_id = serializers.CharField()

    class Meta:
        model = client.V1PortworxVolumeSource


class QuobyteVolumeSource(serializers.Serializer):
    group = serializers.CharField()
    read_only = serializers.BooleanField()
    registry = serializers.CharField()
    tenant = serializers.CharField()
    user = serializers.CharField()
    volume = serializers.CharField()

    class Meta:
        model = client.V1QuobyteVolumeSource


class RBDPersistentVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    image = serializers.CharField()
    keyring = serializers.CharField()
    monitors = serializers.ListField(
        child=serializers.CharField()
    )
    pool = serializers.CharField()
    read_only = serializers.BooleanField()
    secret_ref = SecretReference()
    user = serializers.CharField()

    class Meta:
        model = client.V1RBDPersistentVolumeSource


class ScaleIOPersistentVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    gateway = serializers.CharField()
    protection_domain = serializers.CharField()
    read_only = serializers.BooleanField()
    secret_ref = SecretReference()
    ssl_enabled = serializers.BooleanField()
    storage_mode = serializers.CharField()
    storage_pool = serializers.CharField()
    system = serializers.CharField()
    volume_name = serializers.CharField()

    class Meta:
        model = client.V1ScaleIOPersistentVolumeSource


class StorageOSPersistentVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    read_only = serializers.BooleanField()
    secret_ref = ObjectReference()
    volume_name = serializers.CharField()
    volume_namespace = serializers.CharField()

    class Meta:
        model = client.V1StorageOSPersistentVolumeSource


class VsphereVirtualDiskVolumeSource(serializers.Serializer):
    fs_type = serializers.CharField()
    storage_policy_id = serializers.CharField()
    storage_policy_name = serializers.CharField()
    volume_path = serializers.CharField()
    class Meta:
        model = client.V1VsphereVirtualDiskVolumeSource


class PersistentVolumeClaimSpec(serializers.Serializer):
    access_modes = serializers.ListField(
        child=serializers.CharField()
    )
    aws_elastic_block_store = AWSElasticBlockStoreVolumeSource()
    azure_disk = AzureDiskVolumeSource()
    azure_file = AzureFilePersistentVolumeSource()
    share_name = serializers.DictField()
    cephfs = CephFSPersistentVolumeSource()
    cinder = CinderPersistentVolumeSource()
    claim_ref = ObjectReference()
    csi = CSIPersistentVolumeSource()
    fc = FCVolumeSource()
    flex_volume = FlexPersistentVolumeSource()
    flocker = FlockerVolumeSource()
    gce_persistent_disk = GCEPersistentDiskVolumeSource()
    glusterfs = GlusterfsPersistentVolumeSource()
    host_path = HostPathVolumeSource()
    iscsi = ISCSIPersistentVolumeSource()
    local = LocalVolumeSource()
    mount_options = serializers.ListField(
        child=serializers.CharField()
    )
    nfs = NFSVolumeSource()
    node_affinity = VolumeNodeAffinity()
    persistent_volume_reclaim_policy = serializers.CharField()
    photon_persistent_disk = PhotonPersistentDiskVolumeSource()
    portworx_volume = PortworxVolumeSource()
    quobyte = QuobyteVolumeSource()
    rbd = RBDPersistentVolumeSource()
    scale_io = ScaleIOPersistentVolumeSource()
    storage_class_name = serializers.CharField()
    storageos = StorageOSPersistentVolumeSource()
    volume_mode = serializers.CharField()
    vsphere_volume = VsphereVirtualDiskVolumeSource()

    class Meta:
        model = client.V1PersistentVolumeSpec


class PersistentVolumeClaimCondition(serializers.Serializer):
    last_probe_time = serializers.DateTimeField()
    last_transition_time = serializers.DateTimeField()
    message = serializers.CharField()
    reason = serializers.CharField()
    status = serializers.CharField()
    type = serializers.CharField()

    class Meta:
        model = client.V1PersistentVolumeClaimCondition


class PersistentVolumeClaimStatus(serializers.Serializer):
    access_modes = serializers.ListField(
        child=serializers.CharField()
    )
    allocated_resources = serializers.DictField()
    capacity = serializers.DictField()
    conditions = serializers.ListField(
        child=PersistentVolumeClaimCondition()
    )
    phase = serializers.CharField()
    resize_status = serializers.CharField()

    class Meta:
        model = client.V1PersistentVolumeClaimStatus


class PersistentVolumeClaim(serializers.Serializer):
    api_version = serializers.CharField()
    kind = serializers.CharField()
    metadata = ObjectMeta()
    spec = PersistentVolumeClaimSpec()
    status = PersistentVolumeClaimStatus()

    class Meta:
        model = client.V1PersistentVolumeClaim
