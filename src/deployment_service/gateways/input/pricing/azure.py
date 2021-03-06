from selenium.webdriver import FirefoxOptions
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from deployment_service.config.logging import logger as l

class KubernetesPricingAzure(object):

    def __init__(self):
        self.azure_url ="https://azure.microsoft.com/es-es/pricing/details/kubernetes-service/"
        self.total_price = 0
        self.name = "Microsoft Azure"
        self.price = 0
        self.start_time = ''

    def run(self):
        try:
            self.price = self.get_price()
            self.start_time = time.time()

        except Exception as e:
            print(e,"run")
            l.error('{}: Failed to run Azure pricing for Kubernetes.'.format(e))
            return False
            
    def stop(self):
        try:
            stop_time = time.time()
            elapsed_time = stop_time-self.start_time
            self.total_price = (elapsed_time / 3600) * self.price 
            self.total_price = "{:f}".format(self.total_price)

            return self.total_price


        except Exception as e:
            print(e,"stop")
            l.error('{}: Failed to run Azure pricing for Kubernetes.'.format(e))
            return False

    def get_price(self):
        try:
            opts = FirefoxOptions()
            opts.add_argument("--headless")
            driver = webdriver.Firefox(options=opts)
            driver.get(self.azure_url)
            time.sleep(3)
            price = driver.find_element(By.CLASS_NAME,"price-value")
            price = price.text.replace(",",".")
            driver. quit() 
            self.price = float(price[1:])

            return self.price

        except Exception as e:
            print(e,"get_price")
            print(e)
            l.error('{}: Failed to getting  Azure pricing for Kubernetes.'.format(e))
            return False


