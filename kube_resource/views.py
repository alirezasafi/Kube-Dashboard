from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from kubernetes import client
from .serializers.deployment import Deployment


class DeploymentView(APIView):

    def get(self, request):
        deployment = Deployment()
        response = deployment.list(request.auth)
        response_data = deployment.serialize(response, many=True)
        return Response(data=response_data, status=status.HTTP_200_OK)
