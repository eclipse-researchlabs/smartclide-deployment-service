from datetime import datetime
import random
from kubernetes import client, config, dynamic
from kubernetes.client.exceptions import ApiException
from deployment_service.config.logging import logger as l
from deployment_service.config.settings import Settings
from deployment_service.gateways.input.pricing.provider import KubernetesPricingProvider

class KubernetesDeploymentOutputGateway(object):
    def __init__(self, url, token):
        self.settings = Settings()
        aToken = token
        aConfiguration = client.Configuration()
        aConfiguration.host = url
        aConfiguration.verify_ssl = False
        aConfiguration.api_key = {"authorization": "Bearer " + aToken}

        config.load_config()
        self.aApiClient = client.ApiClient(aConfiguration)
        self.apps_v1_api = client.AppsV1Api(self.aApiClient)
        self.networking_v1_api = client.NetworkingV1Api()

        
    def run(self, name, image, port, replicas, host):
        try:
            self.create_namespace(name.replace('_', '-'))
            deployment = self.create_deployment(name, image, port, replicas)
            self.create_service(name, port)
            # self.create_ingress(name, host, port)
            return deployment

        except Exception as d_ex:
            import traceback; traceback.print_exc()
            l.error('{}: Failed to deploy.'.format(d_ex))
            return d_ex
        

    def stop(self, name):
        try:
            self.delete_deployment(name)
            self.delete_service(name)
            # self.delete_ingress(name)
            return True

        except Exception as d_ex:
            import traceback; traceback.print_exc()
            l.error('{}: Failed to stop deployment.'.format(d_ex))
            return False


    def create_deployment(self, name, image, port, replicas):
        container = client.V1Container(
            name=name,
            image=image,
            image_pull_policy="Never",
            ports=[client.V1ContainerPort(container_port=port)],
        )
        # Template
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": name}),
            spec=client.V1PodSpec(containers=[container]))
        # Spec
        spec = client.V1DeploymentSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(
                match_labels={"app": name}
            ),
            template=template)
        # Deployment
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=name),
            spec=spec)

        deployment = self.apps_v1_api.create_namespaced_deployment(
            namespace=name.replace('_', '-'), 
            body=deployment
        )
        return deployment


    def create_service(self, name, port):
        core_v1_api = client.CoreV1Api()
        body = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(
                name=name
            ),

            spec=client.V1ServiceSpec(
                selector={"app": name},
                ports=[client.V1ServicePort(
                    node_port=random. randint(30000,32767), 
                    port=port,
                    target_port=port
                )], 
                type='NodePort'
            )
        )
        core_v1_api.create_namespaced_service(namespace=name, body=body)
        return True

    def create_ingress(self, name, host, port):
        body = client.V1Ingress(
            api_version="networking.k8s.io/v1",
            kind="Ingress",
            metadata=client.V1ObjectMeta(name=name, annotations={
                "nginx.ingress.kubernetes.io/rewrite-target": "/"
            }),
            spec=client.V1IngressSpec(
                rules=[client.V1IngressRule(
                    host=host,
                    http=client.V1HTTPIngressRuleValue(
                        paths=[client.V1HTTPIngressPath(
                            path="/",
                            path_type="Exact",
                            backend=client.V1IngressBackend(
                                service=client.V1IngressServiceBackend(
                                    port=client.V1ServiceBackendPort(
                                        number=port,
                                    ),
                                    name=name)
                                )
                        )]
                    )
                )
                ]
            )
        )

        self.networking_v1_api.create_namespaced_ingress(namespace=name, body=body)
        return True

    def create_namespace(self, name):
        try:
            client = dynamic.DynamicClient(self.aApiClient)
            namespace_api = client.resources.get(api_version="v1", kind="Namespace")
            namespace_manifest = {
                "apiVersion": "v1",
                "kind": "Namespace",
                "metadata": {
                    "name": name, 
                    "resourceversion": "v1"
                },
            }
            namespace_api.create(body=namespace_manifest)
        except:
            pass

    def delete_deployment(self, name):
        client = dynamic.DynamicClient(self.aApiClient)
        api = client.resources.get(api_version="v1", kind="Deployment")
        service_deleted = api.delete(name=name, body={}, namespace=name)
        return service_deleted
        
    def delete_service(self, name):
        client = dynamic.DynamicClient(self.aApiClient)
        api = client.resources.get(api_version="v1", kind="Service")
        service_deleted = api.delete(name=name, body={}, namespace=name)
        return service_deleted

    def delete_ingress(self, name):
        client = dynamic.DynamicClient(self.aApiClient)
        api = client.resources.get(api_version="v1", kind="Ingress")
        ingress_deleted = api.delete(name=name, body={}, namespace=name)
        return ingress_deleted

    def deployment_status(self, name):
        try:
            client = dynamic.DynamicClient(self.aApiClient)
            api = client.resources.get(api_version="v1", kind="Deployment")
            deployment = api.get(name=name, namespace=name)
            return deployment.status
        except ApiException as ex:
            pass

    def list_deployments(self):
        conf = client.configuration.Configuration()
        with client.ApiClient(self.aApiClient) as api_client:
            api_instance = client.AppsV1Api(self.aApiClient)
            allow_watch_bookmarks = True 
            _continue = '_continue_example' 
            field_selector = 'field_selector_example' 
            label_selector = 'label_selector_example' 
            limit = 56 
            pretty = 'pretty_example' 
            resource_version = 'resource_version_example' 
            resource_version_match = 'resource_version_match_example'
            timeout_seconds = 56
            watch = True
        
        try:
            api_response = api_instance.list_deployment_for_all_namespaces(
                allow_watch_bookmarks=allow_watch_bookmarks, 
                _continue=_continue, 
                field_selector=field_selector, 
                label_selector=label_selector, 
                limit=limit, pretty=pretty, 
                resource_version=resource_version, 
                resource_version_match=resource_version_match, 
                timeout_seconds=timeout_seconds, 
                watch=False)

            l.debug(api_response)
        
        except ApiException as e:
            l.debug("Exception when calling AppsV1Api->list_deployment_for_all_namespaces: %s\n" % e)

    def get_deployment_metrics(self, name, url):
        try:
            config.load_kube_config()
            api = client.CustomObjectsApi()
            k8s_nodes = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")
            for stats in k8s_nodes['items']:
                if name in stats['metadata']['namespace']:
                    pricing_provider = KubernetesPricingProvider(url)
                    prices = pricing_provider.get_prices()
                    date_format_str = '%Y-%m-%dT%H:%M:%SZ'
                    datetime.strptime(stats['metadata']['creationTimestamp'], date_format_str)
                    start = datetime.strptime(stats['metadata']['creationTimestamp'], date_format_str)
                    diff = datetime.now() - start
                    diff_h = diff.total_seconds() / 3600
                    
                    output = {
                        'containers': stats['containers'],
                        "price": { 
                            "current_provider":"",
                            "competitor_provider":[]
                        }
                    }

                    for price in prices:

                        if price['current']:
                            output["price"]['current_provider'] = {
                                'name': price['name'],
                                'price': price['cost'] * diff_h,
                                "cost_type": price['cost_type']
                            }

                        else:
                            output["price"]['competitor_provider'].append({
                                'name': price['name'],
                                'price': price['cost'] * diff_h,
                                "cost_type": price['cost_type']
                            })

                    return output

        except Exception as m_ex:
            import traceback;traceback.print_exc()
            import pdb; pdb.set_trace()