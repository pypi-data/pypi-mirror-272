# Copyright gptvm.ai 2024

import dataclasses
import sys
import click
import inspect
import importlib
from pathlib import Path
from typing import Any, Optional

from ..app import App

DEFAULT_VM_NAME = "app"


class Error(Exception):
    pass


@dataclasses.dataclass
class ImportRef:
    file_or_module: str
    object_path: Optional[str]


def parse_import_ref(object_ref: str) -> ImportRef:
    if object_ref.find("::") > 1:
        file_or_module, object_path = object_ref.split("::", 1)
    elif object_ref.find(":") > 1:
        raise Error(
            f"Invalid object reference: {object_ref}. Did you mean '::' instead of ':'?"
        )
    else:
        file_or_module, object_path = object_ref, None

    return ImportRef(file_or_module, object_path)


class NoSuchObject(Error):
    pass


def import_file_or_module(file_or_module: str):
    if "" not in sys.path:
        # When running from a CLI
        # the current working directory isn't added to sys.path
        # so we add it in order to make module path specification possible
        sys.path.insert(0, "")  # "" means the current working directory
    if file_or_module.endswith(".py"):
        # when using a script path, that scripts directory should also be on the path as it is with `python some/script.py`
        sys.path.insert(0, str(Path(file_or_module).resolve().parent))

        module_name = inspect.getmodulename(file_or_module)
        # Import the module - see https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        spec = importlib.util.spec_from_file_location(module_name, file_or_module)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    else:
        module = importlib.import_module(file_or_module)

    return module


def get_by_object_path(obj: Any, obj_path: str):
    # Note: this is eager, so no backtracking is performed in case an
    # earlier match fails at some later point in the path expansion
    orig_obj = obj
    prefix = ""
    for segment in obj_path.split("."):
        attr = prefix + segment
        try:
            if isinstance(obj, App):
                if attr in obj.registered_entrypoints:
                    # local entrypoints are not on stub blueprint
                    obj = obj.registered_entrypoints[attr]
                    continue
            obj = getattr(obj, attr)

        except Exception:
            prefix = f"{prefix}{segment}."
        else:
            prefix = ""

    if prefix:
        raise NoSuchObject(f"No object {obj_path} could be found in module {orig_obj}")

    return obj


def import_vm(file: str) -> App:
    import_ref = parse_import_ref(file)
    try:
        module = import_file_or_module(import_ref.file_or_module)
        obj_path = (
            import_ref.object_path or DEFAULT_VM_NAME
        )  # get variable named "vm" by default
        vm = get_by_object_path(module, obj_path)
    except NoSuchObject:
        print(f"Could not find object {obj_path} in {import_ref.file_or_module}")
        sys.exit(1)

    if not isinstance(vm, App):
        raise click.UsageError(f"{vm} is not a gptvm VM")

    return vm
