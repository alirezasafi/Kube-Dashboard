from django.urls import path
from .views import DeploymentView, PodView, NameSpaceView, EventView, ReplicaSetView, StatefulSetView

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
    path("replica-set/", ReplicaSetView.as_view({
        "get": "list",
        "post": "create"
    })),
    path("replica-set/<name>/", ReplicaSetView.as_view({
        "get": "retrieve",
        "post": "create"
    })),
    path("stateful-set/", StatefulSetView.as_view({
        "get": "list",
        "post": "create"
    })),
    path("stateful-set/", StatefulSetView.as_view({
        "get": "retrieve",
        "post": "create"
    })),
    path("pod/", PodView.as_view({
        "get": "list",
        "post": "create"
    })),
    path("pod/<name>/", PodView.as_view({
        "get": "retrieve",
        "delete": "destroy"
    })),
    path("event/", EventView.as_view({
        "get": "list"
    })),
    path("event/<name>/", EventView.as_view({
        "get": "retrieve"
    }))
]