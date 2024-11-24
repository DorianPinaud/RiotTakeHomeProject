from abc import ABC, abstractmethod
from typing import Union, Dict, List
import base64
import json


class DecoderStrategy(ABC):

    @abstractmethod
    def decode(self, data: str) -> str:
        pass


class Decoder(ABC):

    @abstractmethod
    def decode(
        self, data: Union[Dict, List], decoding_startegy: DecoderStrategy
    ) -> Union[Dict, List]:
        pass


class OneDepthDecoder(Decoder):

    def decode(
        self, data: Union[Dict, List], decoding_startegy: DecoderStrategy
    ) -> Union[Dict, List]:
        if isinstance(data, list):
            return [
                json.loads(decoding_startegy.decode(item))
                for item in list_data
                if not isinstance(item, str)
            ]
        elif isinstance(data, dict):
            object_data: Dict = data
            return {
                key: json.loads(decoding_startegy.decode(value))
                for key, value in object_data.items()
            }


class Base64DecodingStrategy(DecoderStrategy):

    def decode(self, data: str) -> str:
        base64_byte = data.encode("ascii")
        text_byte = base64.b64decode(base64_byte)
        text = text_byte.decode("ascii")
        return text
