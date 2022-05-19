import os
from decouple import config

class Settings():

    def __init__(self):
        self.repositories = {
            'postgres': {
                'host': 'localhost', 
                'port': 2000, 
                'password': ''
            }
        }
        
        self.api = {
            'host': '0.0.0.0', 
            'port': 6666
        } 

        self.gitlab = {
            'url': os.environ.get('GITLAB_URL',config('GITLAB_URL')),
            'docker_url': 'tcp://docker:2375'
        }

        self.mom = {
            'mom_host': os.environ.get('MOM_HOST',config('MOM_HOST')),
            'mom_port': os.environ.get('MOM_PORT',config('MOM_PORT'))
        }

        self.repo_dir = '/tmp/repos/'
        self.providers = [
            {
                'name': 'generic',
                'url': 'https://192.168.39.183:8443',
                'bearer': 'eyJhbGciOiJSUzI1NiIsImtpZCI6Im9VZ2EtdnR0clMyd1BJM3huRlp6T25TdWFYbEdGQXJqRkFjUXYyX1FFU0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrOHNhZG1pbi10b2tlbi1jcDZyaCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJrOHNhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImFhNTJiM2FlLTA3OGQtNDIyOS1iYWM2LWUzODVkMzIyMjc0ZCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTprOHNhZG1pbiJ9.HSW-I1nvhZ9gvAae0RI3K7Py978SMSsZgEFIE44R7pI1h5VgVGUAL-HKoYBzr8QEv0w0V_HtI_vMZVfOw7sxwcwIz8PU4merA0Hu9MtzphJq_NucZn2HcteSZ43Mdc-cfwMTDzIywIT3SccjDzfllJyyFkgmNP54cVrqko8B7dQR0YLqSYzUWptvDWF_3zpW1r_-y25A9yIZCbDaMshiPgIHh11DCM4V7wVoUlxnWKnqEUZB66OfP4_JthnpV_CcXRru--FGLjY2kpiHrJSexuWTPaqyivSZZu-uos8Vc0ceuCSlCBtAZWFka6myozWU1ALK0g7MoxdkHBGuXjSprA'
            },
            {
                'name': 'AzureAKS',
                'url': 'https://aks-test-dns-bc2e0a2a.hcp.eastus.azmk8s.io/', 
                'bearer': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjdxT3lVUHpRUy1tY1IyOEUyUFh6bFo1UTFZdGdrVThrZnVOaC12NXZsN2cifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrOHNhZG1pbi10b2tlbi1meGJ2bSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJrOHNhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImIzNDM5OTU4LTc2M2UtNDc2Mi05MTA1LWFhMTNkODUxZjZjNSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTprOHNhZG1pbiJ9.taas6D4MZw4qISbtCTeBMBY14Is_6WWFGMHdOQm6mUHFx9_FRCbGNGVSkCEFwawuYtbmwJyQrIjN3nRoIqHwj7cso4kAFsMomp8yaOislCbe8QzNSpeNrzb5hgQNh71OVjHImTplPUHZeyvjVRM6wKKCwo42ISCx56fYQ3CHKXOifxhS3UjL6ddIHRWd1v5yTvj2_84vcgwuC0qkz9qXhZCqaLclPZ6sGHpr0qQvf5YcdpY7ak1k2B8ObSY_mG5cT84UJLNm3y86wxGP0GOVYVIoPhfm2cKehTM7wQZnClphBJth6tVn18ke48HL_EDp3U3fsbXAGs3BkmjSbPaCK1LQMVXzbxinfHFQCDphoTAQYZQtsF_ewHWwnYZy80Z89ujZ_AK5BwtcHhf9zDmU1BdHMEzLiQCc7J8aqfC9Cjv_gzeUYboErsnK_62PQ3-TxS5x6oRPV0K_s_dPayO7Pnko-SlT0OCNsxclbA1l97lweoze40xxiEs3kLHjaylmaHqSN2jufdtyXPD9qjubFadhJ3mW4sRaaTtwY1XpIZkNQ9p0eVqWuVqGLixV7U3EKpeppm17aCa-qBXJdHSDexDOlV6IhEj4MT6qopcxwntKMj2IU3jplDrAWeTWQnwo-o6u2Th2BSpwh7IcU4i8svgEBcc9RUQzMbx_ywBwBLQ'
            }, 
            # 'name': 'GKE': {
            #     'url': '', 
            #     'bearer': ''
            # }, 
            # 'AWSEKS': {
            #     'url': '', 
            #     'bearer': ''
            # }
        ]
        # self.providers = list(filter(lambda provider: provider.get('url') and provider.get('bearer'), __providers))

    def get_job_config(self, job_name, cvs_url, pipeline):
        # return """<?xml version='1.1' encoding='UTF-8'?>
        #     <project>
        #     <builders>
        #         <hudson.tasks.Shell>
        #         <command>echo $JENKINS_VERSION</command>
        #         </hudson.tasks.Shell>
        #     </builders>
        #     </project>"""
        return '''
            <flow-definition plugin="workflow-job@2.41">
            <description> holaaa </description>
            <keepDependencies>falsec</keepDependencies>
            <properties>
            <com.coravy.hudson.plugins.github.GithubProjectProperty plugin="github@1.34.1">
            <projectUrl> https://github.com/pedbermar/wellness_challenge </projectUrl>
            <displayName/>
            </com.coravy.hudson.plugins.github.GithubProjectProperty>
            </properties>
            <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.94">
                <script>
pipeline { 
    agent { dockerfile true } 
    stages { 
        stage('Test') { 
            steps { 
                sh 'node --version' 
                sh 'svn --version' 
            } 
        } 
    } 
} 
</script>
                <sandbox>true</sandbox>
            </definition>
            <triggers/>
            <authToken>z</authToken>
            <disabled>false</disabled>
            </flow-definition>
            
            '''