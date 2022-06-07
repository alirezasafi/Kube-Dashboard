from kubernetes import client
from kubernetes.client.exceptions import ApiException
from rest_framework.exceptions import APIException


class KubeClient:

    apps_v1_list_func_mapping = {
        "DEPLOYMENT": 'list_namespaced_deployment',
    }

    @staticmethod
    def apps_v1_client(configuration):
        return client.AppsV1Api(client.ApiClient(configuration))

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

    def list(self, namespace, selectors, resource_obj, configuration):
        """use apps-v1-client to get the list of resource objects."""
        if resource_obj not in self.apps_v1_list_func_mapping:
            raise ValueError("the resource object isn't valid!")
        func_args = {
            "namespace": namespace,
            **selectors
        }
        return self._make_func_call(
            self.apps_v1_client(configuration),
            self.apps_v1_list_func_mapping[resource_obj],
            **func_args
        )
