import xml.etree.ElementTree as ET
from abc import abstractmethod, ABC
from collections import defaultdict
from typing import Optional, Type, List, TypeVar

from frontpy_core.core.resource_manager_base import ResourceManagerBase
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

    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @abstractmethod
    def find_child_by_id(self, id: int):
        pass


class View(AbstractView, ABC):
    _engine: AbstractEngine = None
    _engine_state_store: AbstractEngineStateStore = None

    def __init__(self, parent: Optional[AbstractView], id=None, **kw_attrs):
        self._id = id
        self._parent = parent
        self._children: List[AbstractView] = []
        self._kw_attrs = kw_attrs
        self._events = defaultdict(list)

    @property
    def id(self):
        id_splits = self._id.split('/')
        if len(id_splits) == 1:
            resource_cat = 'id'
            resource_name = id_splits[0]
        elif len(id_splits) == 2:
            resource_cat, resource_name = id_splits
        else:
            raise KeyError(f"Invalid id: {self._id}. "
                           f"Id should be of format 'name' for view ids, 'resource_cat/name' for other ids.")
        return getattr(getattr(ResourceManagerBase.get_instance(), resource_cat), resource_name)

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

    def find_child_by_id(self, id: int) -> Optional[AbstractView]:
        for child in self.children:
            if child.id == id:
                return child
        for child in self.children:
            target_view = child.find_child_by_id(id)
            if target_view is not None:
                return target_view
        return None

    def add_event_listener(self, event, listener):
        self._events[event].append(listener)
        if self._engine_state_store is not None:
            self._engine.views.generic_view.set_event_listeners(self, self._engine_state_store)


ViewSubclass = TypeVar("ViewSubclass", bound=View)
