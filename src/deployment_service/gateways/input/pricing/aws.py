import boto3
import json
#from deployment_service.config.settings import Settings
from deployment_service.config.logging import logger as l
import time

class KubernetesPricingAWS(object):

    def __init__(self):
        #self.setting = Settings()
        self.aws_access_key_id='AKIAUHL7KHCHVDWI2TCN'
        self.aws_secret_access_key='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'
        self.total_price = 0
        self.price = 0
        self.start_time = ''

    def run(self):
        try:
            self.price = self.get_price()
            self.start_time = time.time()

        except Exception as e:
            print(e)
            l.error('{}: Failed to run AWS pricing for Kubernetes.'.format(e))
            return False
            
    def stop(self):
        try:
            stop_time = time.time()
            elapsed_time = stop_time-self.start_time
            self.total_price = (elapsed_time / 3600) * self.price
            self.total_price = "{:f}".format(self.total_price)

            return self.total_price

        except Exception as e:
            print(e)
            l.error('{}: Failed to run AWS pricing for Kubernetes.'.format(e))
            return False

    def get_price(self,region='eu-west-3'):
        try:
            pricing_client = self.get_pricing_client(self.aws_access_key_id, self.aws_secret_access_key)
            response = pricing_client.describe_services(ServiceCode='AmazonEKS')

            response = pricing_client.get_products(ServiceCode='AmazonEKS')
            list_services = response['PriceList']
            for service in list_services:
                product=json.loads(service)
                product["product"]["attributes"]["servicecode"]   
                OnDemand =  product["terms"]["OnDemand"]
                code_str = list(OnDemand.keys())[0]
                code_dict = product["terms"]["OnDemand"][code_str]["priceDimensions"]
                code_str_2 = list(code_dict.keys())[0]

                if product["product"]["attributes"]["servicename"] == 'Amazon Elastic Container Service for Kubernetes' and product["product"]["attributes"]["regionCode"] == region:   

                    price = OnDemand[code_str]["priceDimensions"][code_str_2]["pricePerUnit"]["USD"]

            return float(price)

        except Exception as e:
            l.error('{}: Failed to getting  AWS pricing for Kubernetes.'.format(e))
            return False

    def get_pricing_client(self,aws_access_key_id,aws_secret_access_key):
        try:
            pricing_client = boto3.client(
                'pricing', 
                region_name='us-east-1',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
            return pricing_client
        except Exception as e:
            print(e)
            l.error('{}: Failed to getting  AWS client for Kubernetes.'.format(e))
            return False

if __name__=="__main__":
    awsPricing = KubernetesPricingAWS()
    awsPricing.run()
    
    time.sleep(20)

    awsPricing.stop()

