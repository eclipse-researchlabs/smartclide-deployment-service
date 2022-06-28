# from kubernetes import client, config
from deployment_service.gateways.output.deploy.kubernetes import KubernetesDeploymentOutputGateway
from kubernetes import config, dynamic, client
from kubernetes.client.exceptions import ApiException

# k8s_url = 'https://192.168.39.96:8443'
# k8s_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6InYtLU5OSjhxMm5tUF9xd2JfOVo3Tm9aa3ktNTlEVXRLeG83d0FhWENHTkUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrOHNhZG1pbi10b2tlbi0yd2JiNiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJrOHNhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImQ5NmJkMTI5LTMyMjEtNDczMy05NjM5LWRhNTA2ZmMyM2EwNCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTprOHNhZG1pbiJ9.Y9jvzFYEaMEoXgwUqS9PLpiHdXiQ1hocaSs7T1r_P4xmSDwp1jYMZXM4PQR2oCpSP8uJnsndRVFPlRrlPKWF4-5A6R7vVlb5CI_0368bp0X-laR4vSv55CL2xit9fma9srfgz7HjLh7hF-fF6lFDWLKsljSeDtXzy59OllPfcaKanRAI4cosc7dqKFB7z_UWMvWaRXU7L_j9pyWyF83hjcoD_47a8EEXZWV3-vYxNng-RGHNn7MY4TcRjimErzrgkZWRhSNBPFKKBu_m15l9QFcefZlOo3yyxFuWecQ-OFRhte1tMtLYS8Ih44qvAYylK6mz9vasejr3CfpoyvVd2Q'
k8s_url = 'https://smartclide-dns-99f66729.hcp.northeurope.azmk8s.io:443'
k8s_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6InEtZVZFWGNiMXFESnIxSVlKQThXTTVNUUxrRFV5YnhXTUp4ZXltTTBuYm8ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrOHNhZG1pbi10b2tlbi04OHg1diIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJrOHNhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImZlNmIzNzJlLTk0ODctNDM5ZS1hYzBlLWNiMGRmYTUzYTM3OCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTprOHNhZG1pbiJ9.d3Gg5uI9QHPeQdLefPK4hiodNiz_vgfRummwbq5QHJzJrcrYSmCiCtMCUuimLjVRKtIa6c2Y0jHIk4bdwMRn6EqfFcIBy4dno7HgT2f2JjYQgvTjP9F_IrmeSYXKirOJAwyl_nhX96XKHNqyucNuEOutWFVYabDRJIZI5V3WLBLusZCQYOLsE43I11u4MMFZJDaYEsKgi_ytVfhb-6onRDwiVBf4sWUrvXejdHSfElOh7zX7cVyMLfyrgQ9W3LzXAVJ5qg6d-7Xt1jvfthFr-5HZVHL5mBwUKMhsb-BLM-5NOckttHaFxQ3SbxSd3B_NrqNXjcfclL9WAKapvI54wrf1rui5DRgQXNZ8zc0fV75i4nkolsK_zWQt754bjmT31HwuIr0Bfu9V1IZPyYa8g1qnEHpy_S3sqUPN2fc40V37IVXA5rCBu84a6RObdNf8pxZlcNuNV8EgG6vQInwJCD-PheR09fclAsN6dBh4Qj21YcNGMPaLsgsuqgWd6SikV5tgIyD9IrVbLwKYUt-1dl8z00RwCi4YHcUh4rFJPR3u11GFz1Ql1mLqb2IWuwKHWrz9DLKg_ysZZ3_1kbuV3Pr0v-eiDZzBrV_iy_AcDmv6VnpgT_EMgn9bQB-4DATLC6EHNrIHUPR1zT_eyqjhfPpnhrJ5T8jUUAAymEktE7M'

class TestKubernetesGateway(object):

    def test_001_constructor(self):
        kd = KubernetesDeploymentOutputGateway(k8s_url, k8s_token)
        assert isinstance(kd, KubernetesDeploymentOutputGateway)


    def test_002_create_deployment(self):
        kd = KubernetesDeploymentOutputGateway(k8s_url, k8s_token)
        d_obj = kd.create_deployment('test-kubernetes', 'pberrocal/test-kubernetes', 8080, 1)
        assert d_obj

    def test_003_create_service(self):
        kd = KubernetesDeploymentOutputGateway(k8s_url, k8s_token)
        s_obj = kd.create_service('test-kubernetes', 8080)
        assert s_obj

    def test_004_create_service(self):
        kd = KubernetesDeploymentOutputGateway(k8s_url, k8s_token)
        i_obj = kd.create_ingress('test-kubernetes', 'test-smartclide.eu', 8080)
        assert i_obj

    def test_005_status(self):
        kd = KubernetesDeploymentOutputGateway(k8s_url, k8s_token)
        replicas = None 
        while replicas == None: 
            replicas = kd.deployment_status('test-kubernetes').replicas

    def test_010_get_deployment_metrics(self):
        kd = KubernetesDeploymentOutputGateway(k8s_url, k8s_token)
        result = kd.get_deployment_metrics('test-kubernetes')
        assert result

    def test_006_delete_deployment(self):
        kd = KubernetesDeploymentOutputGateway(k8s_url, k8s_token)
        d_obj = kd.delete_deployment('test-kubernetes')
        assert d_obj

    def test_007_delete_service(self):
        kd = KubernetesDeploymentOutputGateway(k8s_url, k8s_token)
        s_obj = kd.delete_service('test-kubernetes')
        assert s_obj

    def test_008_delete_service(self):
        kd = KubernetesDeploymentOutputGateway(k8s_url, k8s_token)
        i_obj = kd.delete_ingress('test-kubernetes')
        assert i_obj

    def test_009_run_deployment(self):
        kd = KubernetesDeploymentOutputGateway(k8s_url, k8s_token, '/tmp/repos/wellness_challenge/.gitlab-ci.yml')
        result = kd.run(name='wellness_challenge', image='pberrocal/wellness_challenge', port=6543, replicas=1)
        assert result

    def test_010_stop_deployment(self):
        kd = KubernetesDeploymentOutputGateway(k8s_url, k8s_token)
        result = kd.stop('wellness-challenge')
        assert result
    