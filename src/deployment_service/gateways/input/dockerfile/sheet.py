import json
from urllib import response
from pydantic import Json
import requests

class DockerfileSheet():

    def __init__(self,repo_url):
        self.repo_url = repo_url
        self.first_language = ""
        self.image = ""
        self.dockerfile_sheet =  ""
        
        
    def get_repo_lenguaje(self):

        self.repo_url

        repo_name = self.repo_url.split(".com")[1]+"/languages"

        url = 'https://api.github.com/repos'+repo_name

        response = requests.get(url)

        lenguajes = json.loads(response.text)

        self.first_language = list(lenguajes.keys())[0]

        return self.first_language

        
    def run(self):

        self.get_repo_lenguaje()

        self.generate_dockerfile()

        return self.dockerfile_sheet


    def generate_dockerfile(self):

        json_file = open("./deployment_service/gateways/input/dockerfile/languages.json")

        lenguajes = json.load(json_file)

        if self.first_language in lenguajes.keys():
            self.image = lenguajes[self.first_language]
        else:
            self.image= self.first_language

        self.dockerfile_sheet =  """

                                FROM """+self.image+""" #:version

                                COPY path dst #copy path from the context into the container location(dst)

                                ADD src dst #same as COPY but untar archives and aaccepts http url

                                RUN command args #run a commaand inside the container

                                ENV name=value #set an environment variable

                                WORKDIR path #set the default working directory
                                
                                CMD args #set the default command

                            """

        return self.dockerfile_sheet

