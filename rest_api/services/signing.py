from abc import ABC, abstractmethod
import os
from typing import Dict, Any
import json
import hmac
import hashlib


class SigningStrategy(ABC):

    @abstractmethod
    def sign(self, payload: Any) -> str:
        pass


class HMACSigningStrategy(SigningStrategy):

    def sign(self, payload: Any) -> str:
        secret = os.getenv("SECRET_KEY")
        if not secret:
            # If no key has been setup in the server side just tell the user
            # that the feature is not available
            raise Exception("The signing features is not available yet.")
        data = json.dumps(payload)
        data_bytes = data.encode("ascii")
        secret_bytes = secret.encode()
        hmac_item = hmac.new(secret_bytes, data_bytes, hashlib.sha256)
        return hmac_item.hexdigest()


class SigningStrategyFactory:

    _signing_strategies: Dict

    def __init__(self):
        self._signing_strategies = {"HMAC": HMACSigningStrategy()}

    def create_strategy(self, name: str) -> SigningStrategy:
        if not name in self._signing_strategies:
            raise Exception(f"Signing algorithm '{name}' not implemented by the api")
        return self._signing_strategies[name]


class SigningService:

    _strategy_factory: SigningStrategyFactory

    def __init__(self):
        self._strategy_factory = SigningStrategyFactory()

    def sign(self, payload: Any, algo_name: str = "HMAC") -> str:
        strategy = self._strategy_factory.create_strategy(algo_name)
        return strategy.sign(payload)
