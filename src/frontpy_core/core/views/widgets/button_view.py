from typing import Callable

from frontpy_core.core.views.view import View


class ButtonView(View):
    def __init__(self, parent, **kw_attrs):
        super(ButtonView, self).__init__(parent, **kw_attrs)
        self.text = kw_attrs.get("text")
        self._disabled = kw_attrs.get("disabled", False)
        self._on_click_listener = None

    def on_create(self):
        pass

    def on_start(self):
        self._engine_state_store = self._engine.views.widgets.button_view.create_state_store()
        self._engine.views.widgets.button_view.start_button_view(self, self._engine_state_store)

    def on_stop(self):
        pass

    def on_destroy(self):
        pass

    @property
    def on_click_listener(self):
        return self._on_click_listener

    @on_click_listener.setter
    def on_click_listener(self, value):
        self._on_click_listener = value

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        if self._disabled != value:
            self._disabled = value
            if self._engine_state_store is not None:
                self._engine.views.widgets.button_view.set_disabled(self, self._engine_state_store)
