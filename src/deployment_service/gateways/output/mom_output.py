from logging import setLoggerClass
import time
import paho.mqtt.client as mqtt
import json

from deployment_service.config.logging import logger as l
from deployment_service.config.settings import Settings


class MOMMQTTOutputGateway(object):

    def __init__(self):
        settings = Settings()
        self.__host = settings.mom['mom_host']
        self.__port = int(settings.mom['mom_port'])
        self.SUCCESS = mqtt.MQTT_ERR_SUCCESS
        self.__mqtt_client = self.get_mqtt_client()
    
    
    def get_mqtt_client(self):
        client = mqtt.Client(client_id= "Deployment-component", clean_session=True, userdata=None, transport="tcp")
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message

        client.connect(self.__host, self.__port, 60)
        client.loop_start()
        return client
    
    def publish(self, topic: str, message: str) -> bool:
        try:            
            result_pub = self.__mqtt_client.publish(topic, payload=json.dumps(message))

            pub_ok = False
            if result_pub.rc == mqtt.MQTT_ERR_SUCCESS:
                timeout_counter = 0
                pub_ok = result_pub.is_published()
                import pdb
                pdb.set_trace()
                while not pub_ok and timeout_counter <= 1:
                    time.sleep(0.1)
                    timeout_counter += 0.1
                    pub_ok = result_pub.is_published()

            if pub_ok == False:
                l.error('MQTT did not published the message. RC: ' + result_pub.rc)

            return pub_ok
        except Exception as err:
            return False
    
    def __on_connect(self, client, userdata, flags, rc):
        # Sin subscripciones
        pass

    def __on_message(self, client, userdata, msg):
        # Sin subscripciones
        pass
    
    def send_deployment_is_running(self, service_name, service_id):
        msg = { 
            "header": "start deploy", 
            "service": { 
                "id": service_id, 
                "name": service_name 
            } 

        rc = self.publish('deployment-component', msg)
        return rc
