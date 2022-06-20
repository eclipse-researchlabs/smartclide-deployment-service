from re import M
from deployment_service.gateways.output.mom.amqp import MOMAMQPOutputGateway


class TestMOMOutputGateway(object):

    def test_001_initialize(self):
        mom = MOMAMQPOutputGateway()
        assert mom

    def test_002_send_deployment_is_running_message(self):
        mom = MOMAMQPOutputGateway()
        result = mom.send_deployment_is_running('test-service', 'aaaaaaaaa')
        assert result