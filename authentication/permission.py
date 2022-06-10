from rest_framework.permissions import BasePermission
from kube_client.config import Configuration


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view) -> bool:
        return bool(isinstance(request.auth, Configuration))
