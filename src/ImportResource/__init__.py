# -*- coding: utf-8 -*-


from robotlibcore import keyword, DynamicCore
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.api import logger
from collections import ChainMap
from pathlib import Path
import pkgutil
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


class ImportResource(DynamicCore):
    """ImportResource library provides a wrapper to robotframework so that
    one can use and distribute resource files via python packages.

    For example: if you install python package `foo` via pip that contains a directory `rf-resources`
    you can import all of the resource files into your test suite via

    | `Library` | ImportResource | resources=foo |

    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    RESOURCE_PATH = "rf-resources"

    def __init__(self, resources):
        """
        - ``resources``:
          semicolon separated list of python packages to scan for robotframework resource files
        """

        DynamicCore.__init__(self, [])
        self.resources = []
        try:
            self.rf = BuiltIn()
        except RobotNotRunningError:
            pass
        self.modules = self._find_modules()
        for resource in resources.split(";"):
            if resource in self.modules:
                resource_files = self._find_resources(self.modules[resource])
                if resource_files:
                    for resource_file in resource_files:
                        try:
                            self.rf.import_resource(resource_file)
                        except RobotNotRunningError:
                            pass
                        self.resources.append(resource_file)
                else:
                    logger.warn(f"Module {resource} did't contain any resource files")
            else:
                logger.warn(f"Module {resource} doesn't contain resource directory: {self.RESOURCE_PATH}")

    @keyword
    def external_resources(self):
        """Returns the list of loaded resource file"""
        return [str(item) for item in self.resources]

    def _find_modules(self):
        def is_package(mod):
            return mod.ispkg

        def mod_path(mod):
            return Path(mod.module_finder.path) / Path(mod.name) / Path(self.RESOURCE_PATH)

        def resource_exists(mod):
            return mod[1].is_dir()

        def combine(mods):
            return ChainMap(*mods).items()

        def mod_to_dict(mod):
            return {mod.name: mod_path(mod)}

        return dict(
            filter(
                resource_exists, combine(map(mod_to_dict, filter(is_package, pkgutil.iter_modules())))
            )
        )

    def _find_resources(self, module_path):
        return module_path.rglob("*.resource")
