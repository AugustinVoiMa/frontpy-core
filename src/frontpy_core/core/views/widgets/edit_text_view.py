from frontpy_core.core.views.view import View


class EditTextView(View):
    def __init__(self, parent, **kw_attrs):
        super(EditTextView, self).__init__(parent, **kw_attrs)
        self._text = kw_attrs.get("text")
        self._disabled = kw_attrs.get("disabled", False)
        self._on_edit_listener = None

    def on_create(self):
        pass

    def on_start(self):
        self._engine_state_store = self._engine.views.widgets.edit_text_view.create_state_store()
        self._engine.views.widgets.edit_text_view.start_edit_text_view(self, self._engine_state_store)

    def on_stop(self):
        pass

    def on_destroy(self):
        pass

    @property
    def disabled(self):
        return self._disabled

    @property
    def text(self):
        return self._engine.views.widgets.edit_text_view.current_text(self, self._engine_state_store)

    @text.setter
    def text(self, text):
        self._engine.views.widgets.edit_text_view.update_text(self, self._engine_state_store, text)

    @property
    def on_edit_listener(self):
        return self._on_edit_listener

    @on_edit_listener.setter
    def on_edit_listener(self, value):
        self._on_edit_listener = value
