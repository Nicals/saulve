"""Utility functions for dynamic imports
"""

from importlib import import_module
import importlib.util
from pathlib import Path
from typing import Type, TypeVar

from saulve.errors import MissingAttribute, WrongAttributeType


T = TypeVar('T')


def import_instance(module_name: str, attr: str, cls: Type[T]) -> T:
    """Loads a module, and return one of its attribute.

    Arguments:
        module_name (str): Module to load in dot notation.
        attr (str): Name of the attribute to return.
        cls (type): Expected type of the attribute to return.

    Raises:
        MissingAttribute: If the expected attribute could not be found in the
            imported module.
        WrongAttributeType: If the module attribute isn't of the expected type.
    """
    module = import_module(module_name)

    try:
        instance = getattr(module, attr)
    except AttributeError:
        raise MissingAttribute(module_name, attr)

    if not isinstance(instance, cls):
        raise WrongAttributeType(f'{module_name}.{attr}', cls)

    return instance



def append_module_path(module_name: str, sys_path: list[str]) -> None:
    """Given a module name, if the module is not directly importable tries
    to find if this module exists in the current working directory.
    If so, this directory is added to the python path.
    """
    if importlib.util.find_spec(module_name) is not None:
        return

    cwd = Path.cwd()
    module_path = cwd / module_name

    if not module_path.is_dir() or not (module_path / '__init__.py').is_file():
        return

    sys_path.append(str(cwd))
