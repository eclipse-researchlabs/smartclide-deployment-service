import requests

class KairosInterpreterInputGateway(object):
    def __init__(self):
        self.url = 'http://kairos_interpreter_api:3000/api/v1/'

    def get_jenkins_pipeline(self, cicd_conf_path):
        cicd_conf = {'upload_file': open(cicd_conf_path,'rb')}
        pipeline = requests.post('{}{}'.format(self.url), files=cicd_conf)
        return pipeline

