import xml.etree.ElementTree as ET
import glob
from os.path import join, basename


class InstanceError(Exception):
    pass


class AbstractResourceManager:
    class id:
        pass

    class layout:
        pass


class ResourceManagerBase(AbstractResourceManager):
    __instance = None

    def __init__(self, app_root_path):
        ResourceManagerBase.__instance = self

        self.resources_root = join(app_root_path, 'res')
        self.layouts_root = join(self.resources_root, 'layouts')
        self.layout_retrieve_dict = {}  # associate an id and a layout file to a R.layout uuid
        self._load_layouts_content()

    @staticmethod
    def get_instance() -> AbstractResourceManager:
        if ResourceManagerBase.__instance is None:
            raise InstanceError("ResourceManager was not initialized")
        return ResourceManagerBase.__instance

    @classmethod
    def init_instance(cls, app_root_path):
        if ResourceManagerBase.__instance is not None:
            raise InstanceError("ResourceManager cannot be initialized twice")
        return cls(app_root_path)

    def _load_layouts_content(self):
        for file in glob.glob(join(self.layouts_root, "*.xml"), recursive=False):
            root = ET.parse(file).getroot()
            assert "layout/" in root.attrib["id"]
            _, layout_id = root.attrib["id"].split('/')
            self.layout_retrieve_dict[getattr(self.layout, layout_id)] = dict(layout_file=basename(file),
                                                                              id=layout_id)

    def get_layout_XMLElement(self, layout_id) -> ET.Element:
        file = self.layout_retrieve_dict[layout_id]["layout_file"]
        return ET.parse(join(self.layouts_root, file)).getroot()
