import importlib
from abc import ABC
from os.path import join
from typing import Type

import yaml

from frontpy_core.core.resource_manager_base import ResourceManagerBase
from frontpy_core.engine_base.abstract_engine import AbstractEngine


def load_engine(engine_package_name) -> Type[AbstractEngine]:
    engine_class = importlib.import_module(engine_package_name).Engine
    return engine_class


class BaseApp(ABC):
    def __init__(self, app_root_path):
        with open(join(app_root_path, 'Manifest.yaml')) as yfic:
            self.manifest = yaml.load(yfic, Loader=yaml.SafeLoader)

        engine_class: Type[AbstractEngine] = load_engine(self.manifest["rendering_engine"])
        self._engine = engine_class(self.manifest)

        resource_class: Type[ResourceManagerBase] = importlib.import_module(
            self.manifest["application_package"] + ".R").R
        resource_class.init_instance(app_root_path)  # let the instance created be an object of R of app to keep the ids
        # further calls to ResourceManagerBase.get_instance will return the instance of the app's R

    @property
    def engine(self):
        return self._engine
