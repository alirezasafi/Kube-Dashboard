from kubernetes import client


class KubeClient:

    apps_v1_list_func_mapping = {
        "DEPLOYMENT": 'list_namespaced_deployment',
    }

    @staticmethod
    def apps_v1_client(configuration):
        return client.AppsV1Api(client.ApiClient(configuration))

    def list(self, namespace, resource_obj, configuration):
        """use apps-v1-client to to get the list of resource objects."""
        if resource_obj not in self.apps_v1_list_func_mapping:
            raise ValueError("the resource object isn't valid!")
        response = getattr(
            self.apps_v1_client(configuration),
            self.apps_v1_list_func_mapping[resource_obj]
        )(namespace=namespace)
        return response
