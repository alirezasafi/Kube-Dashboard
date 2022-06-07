from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import deployment, pod


class DeploymentView(ViewSet):
    lookup_field_kwargs = "name"
    serializer_class = deployment.Deployment

    def list(self, request, *args, **kwargs):
        field_selector = request.query_params.get("field", None)
        label_selector = request.query_params.get("label", None)
        namespace = request.query_params.get("namespace", "default")
        selectors = {}
        if field_selector:
            selectors['field_selector'] = field_selector
        if label_selector:
            selectors['label_selector'] = label_selector
        serializer = self.serializer_class()
        response = serializer.list(request.auth, namespace, selectors)
        response_data = serializer.serialize(response, many=True)
        return Response(data=response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        name = kwargs.get(self.lookup_field_kwargs)
        serializer = self.serializer_class()
        response = serializer.get(request.auth, name)
        response_data = serializer.serialize(response)
        return Response(data=response_data, status=status.HTTP_200_OK)


class PodView(ViewSet):
    lookup_field_kwargs = "name"
    serializer_class = pod.Pod

    def list(self, request, *args, **kwargs):
        namespace = request.query_params.get("namespace", "default")
        serializer = self.serializer_class()
        response = serializer.list(request.auth, namespace)
        response_data = serializer.serialize(response)
        return Response(data=response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        name = kwargs.get(self.lookup_field_kwargs)
        serializer = self.serializer_class()
        response = serializer.get(request.auth, name)
        response_data = serializer.serialize(response)
        return Response(data=response_data, status=status.HTTP_200_OK)
