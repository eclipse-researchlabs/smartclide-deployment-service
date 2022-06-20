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
        self.prices = []
        self.provider_url = provider_url
        self.competitor_prices = {}
      
        self.awsPricing = KubernetesPricingAWS()
        self.googlePricing = KubernetesPricingGoogleCloud()
        self.azurePring=KubernetesPricingAzure()

    def get_prices(self):

        try:
            self.get_kubernetes_provider()

            providerArray = [self.awsPricing,self.googlePricing,self.azurePring]

            if self.kubernetes_provider == "Local":
                self.prices.append(
                            {
                            "name":"Local",
                            "cost":0,
                            "current":True, 
                            "cost_type": ""
                            }
                    )

            for provider in providerArray:
                if provider.name == "Amazon Web Service" :
                    self.prices.append(
                        {
                            "name":provider.name,
                            "cost":provider.get_price(),
                            "current":self.kubernetes_provider == provider.name, 
                            "cost_type": "Per CPU"
                        }
                        )
                else:
                    self.prices.append(
                        {
                            "name":provider.name,
                            "cost":provider.get_price(),
                            "current":self.kubernetes_provider == provider.name, 
                            "cost_type": "On Demand"
                            }
                        )
            return self.prices

        except Exception as e:
            l.error('{}: Failed to running Kubernets Pricing Provider for Kubernetes.'.format(e))
            return False

    def get_kubernetes_provider(self):
        try:
            if "azure" in self.provider_url or "microsoft" in self.provider_url:
                self.kubernetes_provider = "Microsoft Azure"
                return

            if "google" in self.provider_url:
                self.kubernetes_provider = "Google Cloud"
                return

            if "aws" in self.provider_url or "amazon" in self.provider_url:
                self.kubernetes_provider = "Amazon Web Service"
                return
            else:
                self.kubernetes_provider = "Local"

        except Exception as e:
            l.error('{}: Failed to getting Kubernets Pricing Provider for Kubernetes.'.format(e))
            return False
