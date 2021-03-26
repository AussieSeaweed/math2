from abc import ABC, abstractmethod


class Region(ABC):
    @abstractmethod
    def integral(self, f):
        pass
