import glob
import os.path
import uuid
import xml.etree.ElementTree as ET
from os.path import join

import yaml
from jinja2 import Template


class ResourceIndexationError(Exception):
    pass


template_str = """
from frontpy_core.core.resource_manager_base import ResourceManagerBase


class R(ResourceManagerBase):
    class id:
{% for id, uuid in ids %}\
        {{ id }} = {{ uuid }}
{% endfor %}\
{% if ids|length == 0 %}\
        pass
{% endif %}\

    class layout:
{% for id, uuid in layouts %}\
        {{ id }} = {{ uuid }}
{% endfor %}\
{% if layouts|length == 0 %}\
        pass
{% endif %}\
"""


class ResourcesIndexer:
    def __init__(self, app_root_path):
        print(app_root_path)
        with open(join(app_root_path, 'Manifest.yaml')) as yfic:
            manifest = yaml.load(yfic, Loader=yaml.SafeLoader)
        self.resources_root = join(app_root_path, "res")
        self.resource_file = join(app_root_path, "src",
                                  manifest["application_package"].replace('.', os.path.sep),
                                  "R.py")
        self.template = Template(template_str)
        self.ids = []
        self.layout_ids = []

    def parse_id(self, id):
        if '/' not in id:
            return None, id
        else:
            type_id, id = id.split('/')
            return type_id, id

    def recursive_indexing(self, e: ET.Element, depth, file):
        if "id" not in e.attrib:
            raise ResourceIndexationError(f"Node '{e.tag}' must define an id in document: {file}")

        id = e.attrib["id"]
        id_type, id = self.parse_id(id)
        if id_type is None:
            if id in self.ids:
                raise ResourceIndexationError(f"Duplicate id: {id} in document {file}")
            self.ids.append(id)
        elif id_type == "layout":
            if id in self.layout_ids:
                raise ResourceIndexationError(f"Duplicate id: {id} in document {file}")
            self.layout_ids.append(id)

        for child in e:
            self.recursive_indexing(child, depth + 1, file)

    def reindex(self):
        try:
            self.ids = []
            self.layout_ids = []

            # index layouts
            for file in glob.glob(join(self.resources_root, "layouts", "**.xml"), recursive=True):
                root = ET.parse(file).getroot()
                self.recursive_indexing(root, 0, file)

            self.ids = [(i, uuid.uuid4().int) for i in self.ids]
            self.layout_ids = [(i, uuid.uuid4().int) for i in self.layout_ids]

            self.generate_resource_file()
        except Exception as e:
            print(e)

    def generate_resource_file(self):
        res = self.template.render(ids=self.ids,
                                   layouts=self.layout_ids)
        with open(self.resource_file, 'w') as rfic:
            rfic.write(res)
