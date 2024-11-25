from abc import ABC, abstractmethod
from typing import Union, Dict, List, Any
import binascii
import base64
import json


class DecryptingStrategy(ABC):

    @abstractmethod
    def decrypt(self, data: Any) -> Dict:
        pass


class Base64DecryptingStrategy(DecryptingStrategy):

    def decrypt(self, data: Any) -> Dict:
        if not isinstance(data, str):
            raise Exception("'base64' format should be string typed to be decrypted")
        try:
            base64_byte = data.encode("ascii")
            text_byte = base64.b64decode(base64_byte)
            text = text_byte.decode("ascii")
            return json.loads(text)
        except ValueError as err:
            raise Exception(
                f"Decryption failed because encrypted data are corrupted: {err}"
            )


class HexDecryptingStrategy(DecryptingStrategy):

    def decrypt(self, data: Any) -> Dict:
        if not isinstance(data, str):
            raise Exception("'hex' format should be string typed to be decrypted")
        try:
            hex_byte = data.encode("ascii")
            text_byte = binascii.unhexlify(hex_byte)
            text = text_byte.decode("ascii")
            return json.loads(text)
        except ValueError as err:
            raise Exception(
                f"Decryption failed because encrypted data are corrupted: {err}"
            )


class DecryptingStrategyFactory:

    _decrypt_strategy: Dict

    def __init__(self):
        self._decrypt_strategy = {
            "base64": Base64DecryptingStrategy(),
            "hex": HexDecryptingStrategy(),
        }

    def create_strategy(self, name: str) -> DecryptingStrategy:
        if not name in self._decrypt_strategy:
            raise Exception(f"Decryption algorithm '{name}' not implemented by the api")
        return self._decrypt_strategy[name]


class DecryptingService:

    _decrypting_strategy_factory: DecryptingStrategyFactory

    def __init__(self):
        self._decrypting_strategy_factory = DecryptingStrategyFactory()

    def decrypt(self, data: Any, decrypting_format: str = "base64") -> Dict:
        if not isinstance(data, dict):
            raise Exception("The data selected for encoding should be an object")
        decrypt_startegy = self._decrypting_strategy_factory.create_strategy(
            decrypting_format
        )
        return {key: decrypt_startegy.decrypt(value) for key, value in data.items()}
