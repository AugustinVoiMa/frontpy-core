from frontpy_core.core.views.layouts.layout import Layout


class LinearLayout(Layout):
    def on_create(self):
        pass

    def on_start(self):
        super(LinearLayout, self).on_start()
        self._engine.views.layouts.linear_layout.linear_layout_start(self, self._engine_state_store)

    def on_stop(self):
        pass

    def on_destroy(self):
        pass

    @property
    def direction(self):
        return self._kw_attrs.get('direction', "vertical")

    @property
    def rtl(self):
        return self._kw_attrs.get('rtl', False)
