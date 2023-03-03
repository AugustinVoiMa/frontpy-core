from abc import ABC
from typing import Union

from frontpy_core.core.views.frame_controller.abstract_frame_controller import AbstractFrameController
from frontpy_core.core.views.view import View, AbstractView


class Layout(View, ABC):
    def __init__(self, parent: Union[AbstractFrameController, AbstractView], **kw_attrs):
        if isinstance(parent, AbstractFrameController):
            self._root = parent
            parent = None
        super(Layout, self).__init__(parent, **kw_attrs)

    @property
    def root(self):
        return self._root

    def on_start(self):
        self._engine_state_store = self._engine.views.layouts.layout.create_state_store()
        self._engine.views.layouts.layout.layout_start(self, self._engine_state_store)
