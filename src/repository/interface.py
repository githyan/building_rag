from abc import ABC, abstractmethod


class abstractRepository(ABC):

    @abstractmethod
    def create_chunks(self, data):
        raise NotImplemented

    @abstractmethod
    def get_chunks(self):
        raise NotImplemented
