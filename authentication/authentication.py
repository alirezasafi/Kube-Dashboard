from rest_framework.authentication import SessionAuthentication
from kube_client.config import KubeConfiguration


class KubeAuthentication(SessionAuthentication):

    def authenticate(self, request):
        token = request.session.get("token")
        if not token:
            return None
        return None, KubeConfiguration.token_configuration(token=token)

