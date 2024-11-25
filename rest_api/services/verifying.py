from abc import ABC, abstractmethod
import os
from typing import Dict, Any
import json
import hmac
import hashlib
from rest_framework.serializers import Serializer, CharField, DictField


class VerifyForm:

    signature: str
    data: Dict

    def __init__(self, signature: str, data: Dict):
        self.signature = signature
        self.data = data


class VerifyFormSerializer(Serializer):
    signature = CharField()
    data = DictField()

    def create(self, validated_data):
        return VerifyForm(**validated_data)


class VerifyingStrategy(ABC):

    @abstractmethod
    def verify(self, payload: Any) -> bool:
        pass


class HMACVerifyingStrategy(VerifyingStrategy):

    def verify(self, verify_form: VerifyForm) -> bool:
        secret = os.getenv("SECRET_KEY")
        if not secret:
            # If no key has been setup in the server side just tell the user
            # that the feature is not available
            raise Exception("The verifying features is not available yet.")
        data = json.dumps(verify_form.data)
        data_bytes = data.encode("ascii")
        secret_bytes = secret.encode()
        hmac_item = hmac.new(secret_bytes, data_bytes, hashlib.sha256)
        return hmac.compare_digest(verify_form.signature, hmac_item.hexdigest())


class VerifyingStrategyFactory:

    _verifying_strategies: Dict

    def __init__(self):
        self._verifying_strategies = {"HMAC": HMACVerifyingStrategy()}

    def create_strategy(self, name: str) -> VerifyingStrategy:
        if not name in self._verifying_strategies:
            raise Exception(f"Verifying algorithm '{name}' not implemented by the api")
        return self._verifying_strategies[name]


class VerifyingService:

    _strategy_factory: VerifyingStrategyFactory

    def __init__(self):
        self._strategy_factory = VerifyingStrategyFactory()

    def verify(self, verify_form: VerifyForm, algo_name: str = "HMAC") -> bool:
        strategy = self._strategy_factory.create_strategy(algo_name)
        return strategy.verify(verify_form)
