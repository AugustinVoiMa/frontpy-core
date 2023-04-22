from abc import abstractmethod, ABC

from frontpy_core.core.views.view import ViewSubclass


class AbstractViewController(ABC):
    @property
    @abstractmethod
    def engine_state_store(self):
        pass

    @abstractmethod
    def find_view_by_id(self, id: int) -> ViewSubclass:
        pass
