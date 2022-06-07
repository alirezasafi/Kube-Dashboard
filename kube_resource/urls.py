from django.urls import path
from .views import DeploymentView

urlpatterns = [
    path("deployment/", DeploymentView.as_view({
        "get": "list"
    })),
    path("deployment/<name>/", DeploymentView.as_view({
        "get": "retrieve"
    })),
]