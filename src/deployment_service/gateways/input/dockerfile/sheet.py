import json
import urllib.parse
import requests
from deployment_service.config.logging import logger as l
from deployment_service.config.settings import Settings
class DockerfileSheet():

    def __init__(self,repo_url, token):
        self.settings = Settings()
        self.repo_url = repo_url
        self.token = token
        self.language = self.get_repo_lenguaje()
        self.image = ""
        
        
    def get_repo_lenguaje(self):
        if self.repo_url[-1] == '/': self.repo_url = self.repo_url[0:-1]
        repo_name = urllib.parse.quote(self.repo_url.split("/")[-1])
        url = '{}api/v4/projects/{}/languages'.format(self.settings.gitlab['url'], repo_name)
        response = requests.get(url, headers={'PRIVATE-TOKEN': self.token})
        lenguajes = json.loads(response.text)
        language = list(lenguajes.keys())[0]
        return language

    def run(self, cloned_repo_path):
        try:
            self.get_repo_lenguaje()
            d_content = self.generate_dockerfile()
            f_path = '{}/Dockerfile'.format(cloned_repo_path)
            f = open(f_path, "w")  
            f.write(d_content)
            f.close()
            return f_path

        except Exception as ex:
            l.error('Failed to write Dockerfile: {}'.format(ex))
            import traceback; traceback.print_exc()



    def generate_dockerfile(self):
        json_file = open("./deployment_service/gateways/input/dockerfile/languages.json")
        lenguajes = json.load(json_file)
        if self.language in lenguajes.keys():
            self.language = lenguajes[self.language]

        dockerfile_sheet =  """

            FROM """+self.language+""" #:version

            COPY path dst #copy path from the context into the container location(dst)

            ADD src dst #same as COPY but untar archives and aaccepts http url

            RUN command args #run a commaand inside the container

            ENV name=value #set an environment variable

            WORKDIR path #set the default working directory
            
            CMD args #set the default command

        """

        return dockerfile_sheet

