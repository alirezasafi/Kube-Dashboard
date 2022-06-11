from kube_client.config import KubeConfiguration
from channels.sessions import SessionMiddleware, CookieMiddleware, InstanceSessionWrapper


class KubeWSSessionMiddleware(SessionMiddleware):

    async def __call__(self, scope, receive, send):
        wrapper = InstanceSessionWrapper(scope, send)

        await wrapper.resolve_session()
        token = wrapper.scope.get("token")
        if token:
            wrapper.scope["auth"] = KubeConfiguration.token_configuration(token=token)

        return await self.inner(wrapper.scope, receive, wrapper.send)


def KubeSessionMiddlewareStack(inner):
    return CookieMiddleware(KubeWSSessionMiddleware(inner))
