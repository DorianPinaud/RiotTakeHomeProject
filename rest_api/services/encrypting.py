from abc import ABC, abstractmethod
from typing import Union, Dict, List, Generator, Tuple, Any
import base64
import json


class EncryptingStrategy(ABC):

    @abstractmethod
    def encrypt(self, data: Any) -> str:
        pass


class Base64EncryptingStrategy(EncryptingStrategy):

    def encrypt(self, data: Any) -> str:
        json_text = json.dumps(data)
        text_bytes = json_text.encode("ascii")
        base64_byte = base64.b64encode(text_bytes)
        base64_text = base64_byte.decode("ascii")
        return base64_text


class EncryptingStrategyFactory:

    _encrypt_strategy: Dict

    def __init__(self):
        self._encrypt_strategy = {"base64": Base64EncryptingStrategy()}

    def create_strategy(self, name: str) -> EncryptingStrategy:
        if not name in self._encrypt_strategy:
            raise Exception(f"Encryption format '{name}' not implemented by the api")
        return self._encrypt_strategy[name]


class EncryptingService:

    def __init__(self):
        self.encrypting_startegy_factory = EncryptingStrategyFactory()

    def encrypt(self, data: Any, encrypting_format: str = "base64") -> Dict:
        if not isinstance(data, dict):
            raise Exception("The data selected for encoding should be an object")
        encrypt_startegy = self.encrypting_startegy_factory.create_strategy(
            encrypting_format
        )
        return {key: encrypt_startegy.encrypt(value) for key, value in data.items()}
