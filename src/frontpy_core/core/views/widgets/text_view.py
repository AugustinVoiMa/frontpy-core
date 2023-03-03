from frontpy_core.core.views.view import View


class TextView(View):
    def __init__(self, parent, **kw_attrs):
        super(TextView, self).__init__(parent, **kw_attrs)
        self.text = kw_attrs.get("text")
        self._disabled = kw_attrs.get("disabled", False)

    def on_create(self):
        pass

    def on_start(self):
        self._engine_state_store = self._engine.views.widgets.text_view.create_state_store()
        self._engine.views.widgets.text_view.start_text_view(self, self._engine_state_store)

    def on_stop(self):
        pass

    def on_destroy(self):
        pass

    @property
    def disabled(self):
        return self._disabled
