import xml.etree.ElementTree as ET
from abc import abstractmethod, ABC
from typing import Optional, Type, List

from frontpy_core.core.utils import get_view_class
from frontpy_core.engine_base.abstract_engine import AbstractEngine
from frontpy_core.engine_base.abstract_state_store import AbstractEngineStateStore


class AbstractView(ABC):

    @abstractmethod
    def on_create(self):
        pass

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_stop(self):
        pass

    @abstractmethod
    def on_destroy(self):
        pass

    @abstractmethod
    def recursive_create(self):
        pass

    @abstractmethod
    def recursive_start(self, depth=0) -> List[str]:
        pass

    @property
    @abstractmethod
    def engine_state_store(self):
        pass


class View(AbstractView, ABC):
    _engine: AbstractEngine = ...
    _engine_state_store: AbstractEngineStateStore = ...

    def __init__(self, parent: Optional[AbstractView], **kw_attrs):
        self._parent = parent
        self._children: List[AbstractView] = []
        self._kw_attrs = kw_attrs

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children.copy()

    def add_child(self, node: AbstractView, index=None):
        if index is None:
            self._children.append(node)
        else:
            self._children.insert(index, node)

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise KeyError("Children of a node can only be referenced by a numeric index")
        return self.children[item]

    def __delitem__(self, key):
        self.pop_child(key)

    def pop_child(self, key):
        return self._children.pop(key)

    def inflate(self, element: ET.Element):
        for i, childElement in enumerate(element):
            view_class: Type[View] = get_view_class(childElement.tag)
            view = view_class(self, xml_index=i, **childElement.attrib)  # self is the parent
            self.add_child(view)
            view.inflate(childElement)

    @staticmethod
    def inject_engine(engine: AbstractEngine):
        View._engine = engine

    def recursive_create(self):
        self.on_create()
        for child in self.children:
            child.recursive_create()

    def recursive_start(self, depth=0):
        self.on_start()
        starts = [
            '\t' * depth + f"| {self.__class__.__name__} (id: {self._kw_attrs.get('id')})"
        ]
        for child in self.children:
            sub_starts = child.recursive_start(depth=depth + 1)
            starts.extend(sub_starts)
        return starts

    @property
    def engine_state_store(self):
        return self._engine_state_store

    @property
    def layout_index(self):
        return self._kw_attrs.get('layout_index', self._kw_attrs['xml_index'])

    @property
    def layout_width(self):
        return self._kw_attrs.get('layout_width', 'match_parent')

    @property
    def layout_height(self):
        return self._kw_attrs.get('layout_height', "wrap_content")