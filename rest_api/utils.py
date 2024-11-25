from __future__ import annotations
from typing import Dict, Any, List


class SingletonMeta(type):

    _instances: Dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ServiceAccessor(metaclass=SingletonMeta):

    _services: Dict

    def __init__(self):
        self._services = {}

    def register(self, service_type: type, params: List = []) -> ServiceAccessor:
        self._services[service_type] = service_type(*params)
        return self

    def get(self, service_type) -> Any:
        return self._services[service_type]
