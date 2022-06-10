from typing import Any, Tuple, Union
from rest_framework.authentication import SessionAuthentication
from kube_client.config import KubeConfiguration, Configuration


class KubeAuthentication(SessionAuthentication):

    def authenticate(self, request) -> Tuple[Any, Union[Any, Configuration]]:
        token = request.session.get("token")
        if not token:
            return None, None
        return None, KubeConfiguration.token_configuration(token=token)

