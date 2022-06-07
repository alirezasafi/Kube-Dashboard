from django.urls import path
from .views import DeploymentView, PodView

urlpatterns = [
    path("deployment/", DeploymentView.as_view({
        "get": "list"
    })),
    path("deployment/<name>/", DeploymentView.as_view({
        "get": "retrieve"
    })),
    path("pod/", PodView.as_view({
        "get": "list"
    })),
    path("pod/<name>/", PodView.as_view({
        "get": "retrieve"
    }))
]