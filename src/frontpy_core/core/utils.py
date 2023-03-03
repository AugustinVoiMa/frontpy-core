import importlib


def get_view_class(node_name):
    nodes_module = importlib.import_module("frontpy_core.core.views")
    if hasattr(nodes_module, node_name):
        return getattr(nodes_module, node_name)
    else:
        raise ImportError(f"View {node_name} was not found in current scope.")


