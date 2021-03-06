from typing import Tuple
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.decorators import action
from authentication.permission import WSIsAuthenticated
from .serializers import deployment, pod, namespace, event, replica_set, stateful_set


class ResourceView(ViewSet):

    def get_selectors(self):
        field_selector = self.request.query_params.get("field", None)
        label_selector = self.request.query_params.get("label", None)
        selectors = {}
        if field_selector:
            selectors['field_selector'] = field_selector
        if label_selector:
            selectors['label_selector'] = label_selector
        return selectors

    def get_client_kwargs(self):
        return {}

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        selectors = self.get_selectors()
        client_kwargs = self.get_client_kwargs()
        serializer.configuration = request.auth
        response = serializer.list(selectors, **client_kwargs)
        response_data = serializer.serialize(response, many=True)
        return Response(data=response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        name = kwargs.get(self.lookup_field_kwargs)
        serializer = self.serializer_class()
        client_kwargs = self.get_client_kwargs()
        serializer.configuration = request.auth
        response = serializer.get(**{"name": name, **client_kwargs})
        response_data = serializer.serialize(response)
        return Response(data=response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        client_kwargs = self.get_client_kwargs()
        serializer.configuration = request.auth
        response = serializer.create_resource(**client_kwargs)
        response_data = serializer.serialize(response)
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        name = kwargs.get(self.lookup_field_kwargs)
        client_kwargs = self.get_client_kwargs()
        serializer = self.serializer_class()
        serializer.configuration = request.auth
        serializer.destroy(name, **client_kwargs)
        return Response(data={"message": "successfully deleted!"}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        name = kwargs.get(self.lookup_field_kwargs)
        client_kwargs = self.get_client_kwargs()
        serializer = self.serializer_class()
        serializer.configuration = request.auth
        response = serializer.patch(name, **client_kwargs)
        response_data = serializer.serialize(response)
        return Response(data=response_data, status=status.HTTP_200_OK)


class NameSpaceView(ResourceView):
    lookup_field_kwargs = "name"
    serializer_class = namespace.Namespace


class DeploymentView(ResourceView):
    lookup_field_kwargs = "name"
    serializer_class = deployment.Deployment

    def get_client_kwargs(self):
        return {"namespace": self.request.query_params.get("namespace", "default")}


class ReplicaSetView(ResourceView):
    lookup_field_kwargs = "name"
    serializer_class = replica_set.ReplicaSet

    def get_client_kwargs(self):
        return {"namespace": self.request.query_params.get("namespace", "default")}


class StatefulSetView(ResourceView):
    lookup_field_kwargs = "name"
    serializer_class = stateful_set.StatefulSet

    def get_client_kwargs(self):
        return {"namespace": self.request.query_params.get("namespace", "default")}


class PodView(ResourceView):
    lookup_field_kwargs = "name"
    serializer_class = pod.Pod

    def get_client_kwargs(self):
        return {"namespace": self.request.query_params.get("namespace", "default")}


class EventView(ResourceView):
    lookup_field_kwargs = "name"
    serializer_class = event.Event

    def get_client_kwargs(self):
        return {"namespace": self.request.query_params.get("namespace", "default")}


class DeploymentAsyncView(GenericAsyncAPIConsumer):
    permission_classes = [WSIsAuthenticated]
    serializer_class = deployment.Deployment

    @action()
    async def status(self, name, **kwargs) -> Tuple[dict, int]:
        serializer = self.serializer_class()
        serializer.configuration = self.scope["auth"]
        response = await serializer.get(**{"name": name})
        response_data = await serializer.serialize(response.status)
        return response_data, status.HTTP_200_OK
