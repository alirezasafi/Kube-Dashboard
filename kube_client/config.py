from django.conf import settings
from kubernetes.config.kube_config import Configuration


class KubeConfiguration(object):

    @classmethod
    def token_configuration(cls, token: str, ca_file: str = None) -> Configuration:
        kube_config = Configuration(
            host=settings.KUBERNETES_HOST,
            api_key={"authorization": "Bearer " + token}
        )
        if ca_file:
            kube_config.ssl_ca_cert = ca_file
        return kube_config
