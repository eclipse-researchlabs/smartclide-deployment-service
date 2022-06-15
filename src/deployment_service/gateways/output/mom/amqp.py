import pika
from deployment_service.gateways.output.mom.output import MOMOutput
from deployment_service.config.logging import logger as l
from deployment_service.config.settings import Settings

class MOMAMQPOutputGateway(MOMOutput):

    def __init__(self):
        settings = Settings()
        self.__host = settings.mom['mom_host']
        self.__port = int(settings.mom['mom_port'])
        self.__amqp_client = self._get_amqp_client()

    def _get_amqp_client(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.__host))
        channel = connection.channel()
        channel.queue_declare(queue='deployment_service')
        return connection
    
    def send_deployment_is_running(self, service_name, service_id):
        try:
            msg = { 
                "header": "start deploy", 
                "service": { 
                    "id": service_id, 
                    "name": service_name 
                } 
            }
            channel = self.__amqp_client.channel()
            channel.basic_publish(
                exchange='',
                routing_key='deployment_service',
                body=str(msg)
            )
            return True

        except Exception as ex:
            l.error(f'{ex}: Failed to send deployment is running mesage to MOM')
            import traceback
            traceback.print_exc()