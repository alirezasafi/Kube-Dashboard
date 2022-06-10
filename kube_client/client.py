from kubernetes import client
from kubernetes.client.exceptions import ApiException
from rest_framework.exceptions import APIException


class AppsV1ApiClient(object):
    list_func_mapping = {
        "DEPLOYMENT": "list_namespaced_deployment",
        "STATEFUL_SET": "list_namespaced_stateful_set",
        "REPLICA_SET": "list_namespaced_replica_set"
    }
    retrieve_func_mapping = {
        "DEPLOYMENT": "read_namespaced_deployment",
        "STATEFUL_SET": "read_namespaced_stateful_set",
        "REPLICA_SET": "read_namespaced_replica_set"
    }
    create_func_mapping = {
        "DEPLOYMENT": "create_namespaced_deployment",
        "STATEFUL_SET": "create_namespaced_stateful_set",
        "REPLICA_SET": "create_namespaced_replica_set"
    }
    delete_func_mapping = {
        "DEPLOYMENT": "delete_namespaced_deployment",
        "STATEFUL_SET": "delete_namespaced_stateful_set",
        "REPLICA_SET": "delete_namespaced_replica_set"
    }
    update_func_mapping = {
        "DEPLOYMENT": "patch_namespaced_deployment",
        "STATEFUL_SET": "patch_namespaced_stateful_set",
        "REPLICA_SET": "patch_namespaced_replica_set"
    }

    @classmethod
    def client(cls, configuration):
        return client.AppsV1Api(client.ApiClient(configuration))


class CoreV1ApiClient(object):
    list_func_mapping = {
        "POD": "list_pod_for_all_namespaces",
        "NAMESPACE": "list_namespace",
        "EVENT": "list_namespaced_event"
    }
    retrieve_func_mapping = {
        "POD": "read_namespaced_pod",
        "NAMESPACE": "read_namespace",
        "EVENT": "read_namespaced_event"
    }
    create_func_mapping = {
        "POD": "create_namespaced_pod",
        "NAMESPACE": "create_namespace"
    }
    delete_func_mapping = {
        "POD": "delete_namespaced_pod",
        "NAMESPACE": "delete_namespace"
    }
    update_func_mapping = {
        "POD": "patch_namespaced_pod",
        "NAMESPACE": "patch_namespace"
    }

    @classmethod
    def client(cls, configuration):
        return client.CoreV1Api(client.ApiClient(configuration))


class KubeClient:
    apps_v1 = AppsV1ApiClient()
    core_v1 = CoreV1ApiClient()

    @staticmethod
    def _make_func_call(api_client, func, **kwargs):
        try:
            response = getattr(
                api_client,
                func
            )(**kwargs)
            return response
        except ApiException as e:
            raise APIException(detail=e.reason, code=e.status)

    def list(self, resource_obj, api_client, configuration, **kwargs):
        """use proper api-client to get the list of resource objects."""
        api_client = getattr(self, api_client)
        if resource_obj not in api_client.list_func_mapping:
            raise ValueError("the resource object isn't valid!")
        return self._make_func_call(
            api_client.client(configuration),
            api_client.list_func_mapping[resource_obj],
            **kwargs
        )

    def get(self, resource_obj, api_client, configuration, **kwargs):
        """use proper api-client to get the resource object details"""
        api_client = getattr(self, api_client)
        if resource_obj not in api_client.retrieve_func_mapping:
            raise ValueError("the resource object isn't valid!")
        return self._make_func_call(
            api_client.client(configuration),
            api_client.retrieve_func_mapping[resource_obj],
            **kwargs
        )

    def create(self, body: object, resource_obj, api_client, configuration, **kwargs):
        """use proper api-client to create the resource element."""
        func_args = {
            "body": body,
            **kwargs
        }
        api_client = getattr(self, api_client)
        if resource_obj not in api_client.create_func_mapping:
            raise ValueError("the resource object isn't valid!")
        return self._make_func_call(
            api_client.client(configuration),
            api_client.create_func_mapping[resource_obj],
            **func_args
        )

    def delete(self, resource_obj, api_client, configuration, **kwargs):
        api_client = getattr(self, api_client)
        if resource_obj not in api_client.delete_func_mapping:
            raise ValueError("the resource object isn't valid!")
        return self._make_func_call(
            api_client.client(configuration),
            api_client.delete_func_mapping[resource_obj],
            **kwargs
        )

    def patch(self, name, body: object, resource_obj, api_client, configuration, **kwargs):
        func_args = {
            "body": body,
            "name": name,
            **kwargs
        }
        api_client = getattr(self, api_client)
        if resource_obj not in api_client.update_func_mapping:
            raise ValueError("the resource object isn't valid!")
        return self._make_func_call(
            api_client.client(configuration),
            api_client.update_func_mapping[resource_obj],
            **func_args
        )
