import json
import requests
import json
#from deployment_service.config.settings import Settings
from deployment_service.config.logging import logger as l
import time

class KubernetesPricingGoogleCloud(object):

    def __init__(self):
        #self.setting = Settings()
        self.google_cloud_access_key='AIzaSyDXVIEfXktSAxvm6YZyHo0lC53esRpQqoE'
        self.google_cloud_url ="https://cloudbilling.googleapis.com/v1/services/CCD8-9BF1-090E/skus"
        self.name = "Google Cloud"
        self.total_price = 0
        self.price = 0
        self.start_time = ''

    def run(self):
        try:
            self.price = self.get_price()
            self.start_time = time.time()

        except Exception as e:
            l.error('{}: Failed to run Google Cloud pricing for Kubernetes.'.format(e))
            return False
            
    def stop(self):
        try:
            stop_time = time.time()
            elapsed_time = stop_time-self.start_time
            self.total_price = (elapsed_time / 3600) * self.price
            self.total_price = "{:f}".format(self.total_price)

            return self.total_price


        except Exception as e:
            l.error('{}: Failed to run Google Cloud pricing for Kubernetes.'.format(e))
            return False

    def get_price(self,region='europe-southwest1'):
        try:
            response = requests.get(self.google_cloud_url+"?key="+self.google_cloud_access_key)
            response = json.loads(response.text)

            for item in response["skus"]:
                if region in item["description"] and item["category"]["usageType"] == "OnDemand":
                    price = item["pricingInfo"][0]["pricingExpression"]["tieredRates"][0]["unitPrice"]["nanos"]

            return float("0."+str(price))

        except Exception as e:
            l.error('{}: Failed to getting  Google Cloud pricing for Kubernetes.'.format(e))
            return False

