import logging
import xml.etree.ElementTree as ET
from typing import Type

from frontpy_core.core.resource_manager_base import ResourceManagerBase
from frontpy_core.core.utils import get_view_class
from frontpy_core.core.views.frame_controller.abstract_view_controller import AbstractViewController
from frontpy_core.core.views.layouts.layout import Layout
from frontpy_core.core.views.view import ViewSubclass
from frontpy_core.engine_base.abstract_engine import AbstractEngine
from frontpy_core.engine_base.abstract_state_store import AbstractEngineStateStore


class FrameControllerError(Exception):
    pass


logger = logging.getLogger(__name__)


class FrameController(AbstractViewController):
    _engine: AbstractEngine = None

    _engine_state_store: AbstractEngineStateStore = None

    def __init__(self):
        self.content_layout: Layout = ...
        self.width = 200
        self.height = 200
        self._title = None

    def set_content_view(self, frame_id: int):
        R = ResourceManagerBase.get_instance()
        root: ET.Element = R.get_layout_XMLElement(frame_id)

        layout_class: Type[Layout] = get_view_class(root.tag)
        if not issubclass(layout_class, Layout):
            raise FrameControllerError("root element of a layout used as a frame layout must be a Layout type")
        layout = layout_class(self, **root.attrib)  # Has no parent
        layout.inflate(root)
        self.content_layout = layout

    def on_create(self):
        self.content_layout.recursive_create()

    def on_start(self):
        self._engine_state_store = self._engine.frame_controller.create_state_store()
        self._engine.frame_controller.start_frame_controller(self, self._engine_state_store)
        starts = ["", "UI Start report",
                  f"Frame Controller (titled: {self.title})"]
        substarts = self.content_layout.recursive_start()

        starts.extend(substarts)
        print('\n'.join(starts))

    @staticmethod
    def inject_engine(engine: AbstractEngine):
        FrameController._engine = engine

    @property
    def engine_state_store(self):
        return self._engine_state_store

    def find_view_by_id(self, id: int) -> ViewSubclass:
        view = self.content_layout.find_child_by_id(id)
        assert view is not None
        return view

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        if self._engine_state_store is None:
            return
        self._engine.frame_controller.set_frame_title(self, self._engine_state_store)
