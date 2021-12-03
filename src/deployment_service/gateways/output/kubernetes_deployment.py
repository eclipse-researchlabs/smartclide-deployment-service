from sqlalchemy.sql import expression
from gitlab.v4.objects import deployments
from kubernetes import config, dynamic, client
from kubernetes.client import api_client
from kubernetes.dynamic.exceptions import ConflictError
from kubernetes.client.exceptions import ApiException
from deployment_service.config.logging import logger as l

class KubernetesDeploymentOutputGateway(object):

    def __init__(self):
        config.load_config()
        self.apps_v1 = client.AppsV1Api()

        
    def deploy(self, project, image, replicas, host, port):
        networking_v1_beta1_api = client.NetworkingV1beta1Api()
        
        try:
            self.create_namespace(project)
        except Exception as err:
            l.error(f'{err}: Failed to create namespace {project}')
            pass

        deployment = self.create_deployment_object(project, image, port, replicas)

        try:
            deployment_result = self.create_deployment(self.apps_v1, deployment, project)            
            service_result = self.create_service(client.CoreV1Api(), port, project)
            ingress_result = self.create_ingress(networking_v1_beta1_api, project, host, port)

            # result = {
            #     'deployment': deployment_result, 
            #     'services': [service_result],
            #     'networking': ingress_result
            # }

            return {
                'code': 200,
                'message': 'Deployment running'
            }        
     
        except ApiException as ex:
            import json 
            return json.loads(ex.body)

        except Exception as ex:
            update_result = self.update_deployment(self.apps_v1, deployment, project)
            return {
                'update': update_result
            }    


    def __get_container_object(self, name, image, port):
        container = client.V1Container(
            name=name,
            image=image,
            ports=[client.V1ContainerPort(container_port=port)],
            resources=client.V1ResourceRequirements(
                requests={"cpu": "100m", "memory": "200Mi"},
                limits={"cpu": "500m", "memory": "500Mi"},
            ),
        )

        return container

    def create_deployment_object(self, project: str, image: str, port: int, replicas):

        container = self.__get_container_object(project, image, port)

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": project}),
            spec=client.V1PodSpec(containers=[container]),
        )

        spec = client.V1DeploymentSpec(
            replicas=replicas, 
            template=template,
            selector = {
                "matchLabels": {"app": project}}
        )

        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=project),
            spec=spec,
        )

        return deployment

    def create_deployment(self, api, deployment, deployment_name):
        resp = api.create_namespaced_deployment(
            body=deployment, namespace=deployment_name
        )

        return resp

    def create_service(self, api, port, service_name):
        body = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(
                name=f'{service_name}-service'
            ),
            spec=client.V1ServiceSpec(
                selector={"app": service_name},
                ports=[client.V1ServicePort(
                    port=80, 
                    target_port=port
                )]
            )
        )

        ret = api.create_namespaced_service(namespace=service_name, body=body)
        return ret

    def create_ingress(self, networking_v1_beta1_api, ingress_name, host, port):
        body = client.NetworkingV1beta1Ingress(
            api_version="networking.k8s.io/v1beta1",
            kind="Ingress",
            metadata=client.V1ObjectMeta(name="{}-ingress".format(ingress_name), annotations={
                    "nginx.ingress.kubernetes.io/rewrite-target": "/",
            }),
            spec=client.NetworkingV1beta1IngressSpec(
                rules=[client.NetworkingV1beta1IngressRule(
                    host=host,
                    http=client.NetworkingV1beta1HTTPIngressRuleValue(
                        paths=[client.NetworkingV1beta1HTTPIngressPath(
                            path="/",
                            backend=client.NetworkingV1beta1IngressBackend(
                                service_port=80,
                                service_name='{}-service'.format(ingress_name),
                            )
                        )]
                    )
                )]
            )
        )

        ret = networking_v1_beta1_api.create_namespaced_ingress(
            namespace=ingress_name,
            body=body
        )
        return ret
        
    def update_deployment(self, api, deployment, deployment_name):
        resp = api.patch_namespaced_deployment(
            name=deployment_name, namespace=deployment_name, body=deployment
        )
        
        result = {
            'replicas': resp.status.replicas,
            'ready_replicas': resp.status.ready_replicas, 
            'updated_replicas': resp.status.updated_replicas, 
            'unavailable_replicas': resp.status.unavailable_replicas
        }
        return result

    def delete_deployment(self, deployment_name):
        # Delete deployment
        self.delete_service(deployment_name)
        self.delete_ingress(deployment_name)
        api = self.__get_api('Deployment')
        resp = api.delete(deployment_name, deployment_name)
        return resp 
    
    def delete_service(self, name):
        client = dynamic.DynamicClient(
            api_client.ApiClient(configuration=config.load_config())
        )
        api = client.resources.get(api_version="v1", kind="Service")
        service_deleted = api.delete(name=f'{name}-service', body={}, namespace=name)
        return service_deleted

    def delete_ingress(self, name):
        client = dynamic.DynamicClient(
            api_client.ApiClient(configuration=config.load_config())
        )
        # fetching the service api
        api = client.resources.get(api_version="v1", kind="Ingress")
        ingress_deleted = api.delete(name=f'{name}-ingress', body={}, namespace=name)
        return ingress_deleted

    def deployment_status(self, deployment_name):
        try:
            api = self.__get_api('Deployment')
            deployment = api.get(name=deployment_name, namespace=deployment_name)
            return deployment.status

        except ApiException as ex:
            return ex

    def create_namespace(self, name):
        # Creating a dynamic client
        client = dynamic.DynamicClient(
            api_client.ApiClient(configuration=config.load_kube_config())
        )

        crd_api = client.resources.get(
            api_version="apiextensions.k8s.io/v1", kind="CustomResourceDefinition"
        )

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

    def __get_api(self, resource):
        d_client = dynamic.DynamicClient(
            api_client.ApiClient(
                configuration=config.load_kube_config()
            )
        )
        api = d_client.resources.get(api_version="apps/v1", kind=resource)
        return api

    def get_deployment_metrics(self, name):
        config.load_kube_config()
        api = client.CustomObjectsApi()
        k8s_nodes = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")

        for stats in k8s_nodes['items']:
            if name in stats['metadata']['namespace']:
                return stats['containers']                


    def get_token(self, region_name: str ='us-west-2', aws_access_key_id: str ='AKIAUHL7KHCHVDWI2TCN', aws_secret_access_key: str = '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'):
        eks_client = boto3.client(
            'eks',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        eks_details = eks_client.describe_cluster(name='my_cluster')['cluster']
