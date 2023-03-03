from abc import ABC, abstractmethod
from typing import List

from . import frame_controller
from . import views


class AbstractEngine(ABC):
    views = views
    frame_controller = frame_controller

    def __init__(self, manifest):
        self.manifest = manifest

    @abstractmethod
    def launch_frames(self) -> List:
        pass

    @abstractmethod
    def run(self):
        pass
