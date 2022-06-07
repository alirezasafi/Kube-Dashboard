from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers.deployment import Deployment


class DeploymentView(ViewSet):
    serializer_class = Deployment

    def list(self, request, *args, **kwargs):
        field_selector = request.query_params.get("field", None)
        label_selector = request.query_params.get("label", None)
        namespace = request.query_params.get("namespace", "default")
        selectors = {}
        if field_selector:
            selectors['field_selector'] = field_selector
        if label_selector:
            selectors['label_selector'] = label_selector
        deployment = self.serializer_class()
        response = deployment.list(request.auth, namespace, selectors)
        response_data = deployment.serialize(response, many=True)
        return Response(data=response_data, status=status.HTTP_200_OK)
