import os 
import sys

from deployment_service.gateways.input.api.metrics import router as metrics_router
from deployment_service.gateways.input.api.deployments import router as deployments_router
from deployment_service.gateways.input.api.builds import router as builds_router
from deployment_service.gateways.input.api.providers import router as providers_router
from fastapi import FastAPI
from fastapi.testclient import TestClient

# settings = Settings()

api = FastAPI(title="SmartCLIDE deployment component API")

api.include_router(deployments_router)
api.include_router(metrics_router)

client = TestClient(api)

class TestAPIDeploymentEndpoints(object):
    def test_001_get_deployments(self):
        response = client.get("/deployments/?user=pberrocal&project=test-kubernetes&skip=0&limit=10")
        assert response.status_code == 200


    def test_003_post_deployments(self):
        response = client.post(
            "deployments/?user=pberrocal&git_repo_url=https%3A%2F%2Fgitlab.dev.smartclide.eu%2F&project_name=test-kubernetes&k8s_url=https%3A%2F%2F192.168.39.96%3A8443&hostname=test-smartclide.eu&branch=master&replicas=1&deployment_port=8080", 
            headers={"k8s-token": "eyJhbGciOiJSUzI1NiIsImtpZCI6InYtLU5OSjhxMm5tUF9xd2JfOVo3Tm9aa3ktNTlEVXRLeG83d0FhWENHTkUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrOHNhZG1pbi10b2tlbi0yd2JiNiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJrOHNhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImQ5NmJkMTI5LTMyMjEtNDczMy05NjM5LWRhNTA2ZmMyM2EwNCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTprOHNhZG1pbiJ9.Y9jvzFYEaMEoXgwUqS9PLpiHdXiQ1hocaSs7T1r_P4xmSDwp1jYMZXM4PQR2oCpSP8uJnsndRVFPlRrlPKWF4-5A6R7vVlb5CI_0368bp0X-laR4vSv55CL2xit9fma9srfgz7HjLh7hF-fF6lFDWLKsljSeDtXzy59OllPfcaKanRAI4cosc7dqKFB7z_UWMvWaRXU7L_j9pyWyF83hjcoD_47a8EEXZWV3-vYxNng-RGHNn7MY4TcRjimErzrgkZWRhSNBPFKKBu_m15l9QFcefZlOo3yyxFuWecQ-OFRhte1tMtLYS8Ih44qvAYylK6mz9vasejr3CfpoyvVd2Q"}
        )

        assert response.status_code == 200

    def test_002_get_deployment(self):
        response = client.get(
            "/deployments/38c66e7b-a7ec-430e-8937-03f43627812b", 
            headers={"k8s-token": "eyJhbGciOiJSUzI1NiIsImtpZCI6InYtLU5OSjhxMm5tUF9xd2JfOVo3Tm9aa3ktNTlEVXRLeG83d0FhWENHTkUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrOHNhZG1pbi10b2tlbi0yd2JiNiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJrOHNhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImQ5NmJkMTI5LTMyMjEtNDczMy05NjM5LWRhNTA2ZmMyM2EwNCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTprOHNhZG1pbiJ9.Y9jvzFYEaMEoXgwUqS9PLpiHdXiQ1hocaSs7T1r_P4xmSDwp1jYMZXM4PQR2oCpSP8uJnsndRVFPlRrlPKWF4-5A6R7vVlb5CI_0368bp0X-laR4vSv55CL2xit9fma9srfgz7HjLh7hF-fF6lFDWLKsljSeDtXzy59OllPfcaKanRAI4cosc7dqKFB7z_UWMvWaRXU7L_j9pyWyF83hjcoD_47a8EEXZWV3-vYxNng-RGHNn7MY4TcRjimErzrgkZWRhSNBPFKKBu_m15l9QFcefZlOo3yyxFuWecQ-OFRhte1tMtLYS8Ih44qvAYylK6mz9vasejr3CfpoyvVd2Q"}
        )
        
        assert response.status_code == 200

