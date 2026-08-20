import importlib
import inspect
from pathlib import Path

from polaris.plugins.base import BasePlugin


class PluginManager:
    def __init__(self):
        self.plugins = {}

    def discover(self):
        base_path = Path(__file__).resolve().parents[2]
        plugin_root = base_path / "polaris" / "plugins"

        for file in plugin_root.rglob("plugin.py"):
            relative = file.relative_to(base_path)

            module_name = ".".join(relative.with_suffix("").parts)

            module = importlib.import_module(module_name)

            for _, obj in inspect.getmembers(
                module,
                inspect.isclass,
            ):
                if (
                    issubclass(obj, BasePlugin)
                    and obj is not BasePlugin
                    and hasattr(obj, "name")
                ):
                    self.plugins[obj.name] = obj()

        return self.plugins
