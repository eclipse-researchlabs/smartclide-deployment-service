import time

from click import option 
from deployment_service.gateways.input.pricing.aws import KubernetesPricingAWS
from deployment_service.gateways.input.pricing.azure import KubernetesPricingAzure
from deployment_service.gateways.input.pricing.google_cloud import KubernetesPricingGoogleCloud
#from deployment_service.config.settings import Settings
from deployment_service.config.logging import logger as l


class KubernetesPricingProvider():

    def __init__(self,provider_url):
        #self.setting = Settings()
        self.kubernetes_provider= ""
        self.total_price = 0
        self.provider_url = provider_url
        self.competitor_prices = {}
      
        self.kubernetes_competitor_provider_1= ""
        self.kubernetes_competitor_provider_1_name= ""
        self.price_competitor_1 = 0
        
        self.kubernetes_competitor_provider_2= ""
        self.kubernetes_competitor_provider_2_name= ""
        self.price_competitor_2 = 0

    def run(self):
        try:
            self.get_kubernetes_provider()

            self.kubernetes_provider.run()

            self.get_competitor_prices(option="run")
        except Exception as e:
            l.error('{}: Failed to running Kubernets Pricing Provider for Kubernetes.'.format(e))
            return False


    def stop(self):
        try:
            self.total_price = self.kubernetes_provider.stop()

            self.get_competitor_prices(option="stop")

            print(self.competitor_prices,"precios competidor")

            print(self.total_price,"precio_total")
            return self.total_price
        except Exception as e:
            l.error('{}: Failed to stopping Kubernets Pricing Provider for Kubernetes.'.format(e))
            return False


    def get_competitor_prices(self,option):
        try:
            if option == "run":
                if type(self.kubernetes_provider) == KubernetesPricingAzure:
                    self.kubernetes_competitor_provider_1 = KubernetesPricingAWS()
                    self.kubernetes_competitor_provider_1_name = "Amazon Web Service"
                    
                    self.kubernetes_competitor_provider_2 = KubernetesPricingGoogleCloud()
                    self.kubernetes_competitor_provider_2_name = "Google Cloud"


                    self.kubernetes_competitor_provider_1.run()
                    self.kubernetes_competitor_provider_2.run()


                if type(self.kubernetes_provider) == KubernetesPricingAWS:
                    self.kubernetes_competitor_provider_1 = KubernetesPricingAzure()
                    self.kubernetes_competitor_provider_1_name = "Microsoft Azure"

                    self.kubernetes_competitor_provider_2 = KubernetesPricingGoogleCloud()
                    self.kubernetes_competitor_provider_2_name = "Google Cloud"

                    self.kubernetes_competitor_provider_1.run()
                    self.kubernetes_competitor_provider_2.run()


                if type(self.kubernetes_provider) == KubernetesPricingGoogleCloud:
                    self.kubernetes_competitor_provider_1 = KubernetesPricingAWS()
                    self.kubernetes_competitor_provider_1_name = "Amazon Web Service"

                    self.kubernetes_competitor_provider_2 = KubernetesPricingAzure()
                    self.kubernetes_competitor_provider_2_name = "Microsoft Azure"

                    self.kubernetes_competitor_provider_1.run()
                    self.kubernetes_competitor_provider_2.run()

            if option == "stop":
                self.price_competitor_1 = self.kubernetes_competitor_provider_1.stop()
                self.price_competitor_2 = self.kubernetes_competitor_provider_2.stop()
                
                self.competitor_prices =  {self.kubernetes_competitor_provider_1_name:self.price_competitor_1,self.kubernetes_competitor_provider_2_name:self.price_competitor_2}

                return {self.kubernetes_competitor_provider_1_name:self.price_competitor_1,self.kubernetes_competitor_provider_2_name:self.price_competitor_2}

        except Exception as e:
            l.error('{}: Failed to getting Kubernets Competitor Prices for Kubernetes.'.format(e))
            return False


    def get_kubernetes_provider(self):
        try:
            if "azure" in self.provider_url or "microsoft" in self.provider_url:
                self.kubernetes_provider = KubernetesPricingAzure()

            if "google" in self.provider_url:
                self.kubernetes_provider = KubernetesPricingGoogleCloud()

            if "aws" in self.provider_url or "amazon" in self.provider_url:
                self.kubernetes_provider = KubernetesPricingAWS()

        except Exception as e:
            l.error('{}: Failed to getting Kubernets Pricing Provider for Kubernetes.'.format(e))
            return False

if __name__ == "__main__":
    pricingKubernets = KubernetesPricingProvider("https://container.googleapis.com")
    pricingKubernets.run()

    time.sleep(10)

    pricingKubernets.stop()