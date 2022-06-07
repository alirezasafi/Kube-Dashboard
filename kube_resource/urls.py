from django.urls import path
from .views import DeploymentView, PodView, NameSpaceView

urlpatterns = [
    path("namespace/", NameSpaceView.as_view({
        "get": "list"
    })),
    path("namespace/<name>/", NameSpaceView.as_view({
        "get": "retrieve"
    })),
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