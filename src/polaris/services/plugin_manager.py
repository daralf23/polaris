import importlib
import inspect
from pathlib import Path

from polaris.plugins.base import BasePlugin


class PluginManager:
    def __init__(self):
        self.plugins = {}

    def discover(self):
        base_path = Path(__file__).resolve().parents[2]  # .../src
        plugin_root = base_path / "polaris" / "plugins"

        for file in plugin_root.rglob("plugin.py"):
            # Convert file path → module path
            relative = file.relative_to(base_path)

            module_name = ".".join(relative.with_suffix("").parts)

            # IMPORTANT: module_name now starts with "polaris..."
            module = importlib.import_module(module_name)

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    issubclass(obj, BasePlugin)
                    and obj is not BasePlugin
                    and hasattr(obj, "name")
                ):
                    self.plugins[obj.name] = obj()

        return self.plugins
