from django.urls import path
from .views import DeploymentView, PodView, NameSpaceView

urlpatterns = [
    path("namespace/", NameSpaceView.as_view({
        "get": "list",
        "post": "create"
    })),
    path("namespace/<name>/", NameSpaceView.as_view({
        "get": "retrieve",
        "delete": "destroy"
    })),
    path("deployment/", DeploymentView.as_view({
        "get": "list",
        "post": "create"
    })),
    path("deployment/<name>/", DeploymentView.as_view({
        "get": "retrieve",
        "delete": "destroy"
    })),
    path("pod/", PodView.as_view({
        "get": "list",
        "post": "create"
    })),
    path("pod/<name>/", PodView.as_view({
        "get": "retrieve",
        "delete": "destroy"
    }))
]