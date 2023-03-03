from frontpy_core.core.abstract_app import BaseApp
from frontpy_core.core.views.frame_controller.frame_controller import FrameController
from frontpy_core.core.views.view import View
from frontpy_core.engine_base.abstract_engine import AbstractEngine


def inject_engine(engine: AbstractEngine):
    FrameController.inject_engine(engine)
    View.inject_engine(engine)


class App(BaseApp):
    def launch(self):
        inject_engine(self.engine)

        open_frames_sequence = self.engine.launch_frames()

        for frame in open_frames_sequence:
            frame.on_create()
            frame.on_start()

        self.engine.run()
