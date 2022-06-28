import json
import requests
from deployment_service.config.logging import logger as l

class DockerfileSheet():

    def __init__(self,repo_url):
        self.repo_url = repo_url
        self.language = self.get_repo_lenguaje()
        self.image = ""
        
        
    def get_repo_lenguaje(self):
        repo_name = self.repo_url.split(".com")[1]+"/languages"
        url = 'https://api.github.com/repos/{}'.format(repo_name)
        response = requests.get(url)
        lenguajes = json.loads(response.text)
        language = list(lenguajes.keys())[0]
        return language

    def run(self, cloned_repo_path):
        try:
            self.get_repo_lenguaje()
            d_content = self.generate_dockerfile()
            f_path = '{}/Dockerfile'.fortmat(cloned_repo_path)
            f = open(f_path, "w")  
            f.write(d_content)
            f.close()
            return f_path

        except Exception as ex:
            l.error('Failed to write Dockerfile to {}: {}'.format(f_path, ex))
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

