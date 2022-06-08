from kubernetes import client
from kubernetes.client.exceptions import ApiException
from rest_framework.exceptions import APIException


class AppsV1ApiClient(object):
    list_func_mapping = {
        "DEPLOYMENT": "list_namespaced_deployment"
    }
    retrieve_func_mapping = {
        "DEPLOYMENT": "read_namespaced_deployment"
    }
    create_func_mapping = {
        "DEPLOYMENT": "create_namespaced_deployment"
    }

    @classmethod
    def client(cls, configuration):
        return client.AppsV1Api(client.ApiClient(configuration))


class CoreV1ApiClient(object):
    list_func_mapping = {
        "POD": "list_pod_for_all_namespaces",
        "NAMESPACE": "list_namespace"
    }
    retrieve_func_mapping = {
        "POD": "read_namespaced_pod",
        "NAMESPACE": "read_namespace"
    }
    create_func_mapping = {
        "POD": "create_namespaced_pod",
        "NAMESPACE": "create_namespace"
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