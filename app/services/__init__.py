import inspect
import sys

from .dbmanager import DBManager
from .etherscan import Etherscan

_cached_services = {}


def get_service(service_class):
    global _cached_services
    if service_class not in _cached_services:
        _cached_services[service_class] = service_class()
    return _cached_services[service_class]


def get_dbmanager() -> DBManager:
    return get_service(DBManager)


def get_etherscan() -> Etherscan:
    return get_service(Etherscan)


def make_getter(cls):
    def getter():
        return get_service(cls)

    return getter


_current_module = sys.modules[__name__]

for name, cls in inspect.getmembers(_current_module, inspect.isclass):
    if cls.__module__ == __name__:
        function_name = f"get_{name.lower()}"
        globals()[function_name] = make_getter(cls)

__all__ = [
    f"get_{name.lower()}"
    for name, cls in inspect.getmembers(_current_module, inspect.isclass)
]
