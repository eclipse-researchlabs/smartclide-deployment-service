from abc import ABC, abstractmethod

class MOMOutput(ABC):
    @abstractmethod
    def send_deployment_is_running(self):
        ...