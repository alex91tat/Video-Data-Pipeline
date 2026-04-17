from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass