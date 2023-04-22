from abc import ABC
from typing import Union

from frontpy_core.core.views.frame_controller.abstract_view_controller import AbstractViewController
from frontpy_core.core.views.view import View, AbstractView


class Layout(View, ABC):
    def __init__(self, parent: Union[AbstractViewController, AbstractView], **kw_attrs):
        if isinstance(parent, AbstractViewController):
            self._root = parent
            parent = None
        super(Layout, self).__init__(parent, **kw_attrs)

    @property
    def root(self):
        return self._root

    def on_start(self):
        self._engine_state_store = self._engine.views.layouts.layout.create_state_store()
        self._engine.views.layouts.layout.layout_start(self, self._engine_state_store)
