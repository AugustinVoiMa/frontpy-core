from abc import abstractmethod, ABC


class AbstractFrameController(ABC):
    @property
    @abstractmethod
    def engine_state_store(self):
        pass
