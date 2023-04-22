from frontpy_core.engine_base.abstract_state_store import AbstractEngineStateStore
from frontpy_core.engine_base.meta import AbstractEngineException


def create_state_store() -> AbstractEngineStateStore:
    raise AbstractEngineException


def start_edit_text_view(view, state_store):
    raise AbstractEngineException


def update_text(view, state_store):
    raise AbstractEngineException
