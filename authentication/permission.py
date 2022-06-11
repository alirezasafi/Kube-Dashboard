from typing import Dict, Any
from rest_framework.permissions import BasePermission
from djangochannelsrestframework.permissions import BasePermission as WSBasePermission
from channels.consumer import AsyncConsumer
from kube_client.config import Configuration


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view) -> bool:
        return bool(isinstance(request.auth, Configuration))


class WSIsAuthenticated(WSBasePermission):
    async def has_permission(
        self, scope: Dict[str, Any], consumer: AsyncConsumer, action: str, **kwargs
    ) -> bool:
        return True
