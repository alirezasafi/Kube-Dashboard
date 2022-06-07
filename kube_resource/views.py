from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import deployment, pod, namespace


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


class NameSpaceView(ResourceView):
    lookup_field_kwargs = "name"
    serializer_class = namespace.Namespace

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        selectors = self.get_selectors()
        response = serializer.list(request.auth, selectors)
        response_data = serializer.serialize(response, many=True)
        return Response(data=response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        name = kwargs.get(self.lookup_field_kwargs)
        serializer = self.serializer_class()
        response = serializer.get(request.auth, name)
        response_data = serializer.serialize(response)
        return Response(data=response_data, status=status.HTTP_200_OK)


class DeploymentView(ResourceView):
    lookup_field_kwargs = "name"
    serializer_class = deployment.Deployment

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        client_kwargs = {"namespace": request.query_params.get("namespace", "default")}
        selectors = self.get_selectors()
        response = serializer.list(request.auth, selectors, **client_kwargs)
        response_data = serializer.serialize(response, many=True)
        return Response(data=response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        name = kwargs.get(self.lookup_field_kwargs)
        serializer = self.serializer_class()
        response = serializer.get(request.auth, name)
        response_data = serializer.serialize(response)
        return Response(data=response_data, status=status.HTTP_200_OK)


class PodView(ResourceView):
    lookup_field_kwargs = "name"
    serializer_class = pod.Pod

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        selectors = self.get_selectors()
        response = serializer.list(request.auth, selectors)
        response_data = serializer.serialize(response, many=True)
        return Response(data=response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        name = kwargs.get(self.lookup_field_kwargs)
        serializer = self.serializer_class()
        response = serializer.get(request.auth, name)
        response_data = serializer.serialize(response)
        return Response(data=response_data, status=status.HTTP_200_OK)
