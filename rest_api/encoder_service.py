from abc import ABC, abstractmethod
from typing import Union, Dict, List
import base64
import json


class EncoderStrategy(ABC):

    @abstractmethod
    def encode(self, data: str) -> str:
        pass


class Encoder(ABC):

    @abstractmethod
    def encode(self, data: Union[Dict, List], encoding_startegy) -> Union[Dict, List]:
        pass


class OneDepthEncoder(Encoder):

    def encode(
        self, data: Union[Dict, List], encoding_startegy: EncoderStrategy
    ) -> Union[Dict, List]:
        if isinstance(data, list):
            list_data: List = data
            return [encoding_startegy.encode(json.dumps(item)) for item in list_data]
        elif isinstance(data, dict):
            object_data: Dict = data
            return {
                key: encoding_startegy.encode(json.dumps(value))
                for key, value in object_data.items()
            }


class Base64EncodingStrategy(EncoderStrategy):

    def encode(self, data: str) -> str:
        text_bytes = data.encode("ascii")
        base64_byte = base64.b64encode(text_bytes)
        base64_text = base64_byte.decode("ascii")
        return base64_text


class EncoderStrategyFactory:

    _encoder_strategy: Dict

    def __init__(self):
        self._encoder_strategy = {"base64": Base64EncodingStrategy()}

    def create_strategy(self, name: str = "base64") -> EncoderStrategy:
        if not name in self._encoder_strategy:
            raise Exception(f"Encryption format '{name}' not implemented by the api")
        return self._encoder_strategy[name]
