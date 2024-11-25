from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
import base64
import json
from .services.rate_limiting import (
    RateLimitService,
    RateLimitTracker,
    TimeRateLimitTrackerFactory,
)

from .services.decrypting import DecryptingService
from .services.encrypting import EncryptingService
from .services.signing import SigningService
from .utils import ServiceAccessor

ServiceAccessor().register(
    RateLimitService,
    [
        TimeRateLimitTrackerFactory(max_limit_in_second=1, max_usage_per_second=60),
    ],
).register(DecryptingService).register(EncryptingService).register(SigningService)


@api_view(["POST"])
def encryption_endpoint(request: Request):
    rate_limit_service: RateLimitService = ServiceAccessor().get(RateLimitService)
    encryption_service: EncryptingService = ServiceAccessor().get(EncryptingService)
    if not rate_limit_service.get_tracked_user(request.META["REMOTE_ADDR"]).attempt():
        return Response(
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )
    algo_param = request.query_params.get("algo", "base64")
    try:
        return Response(encryption_service.encrypt(request.data, algo_param))
    except Exception as err:
        return Response({"info": str(err)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["post"])
def decryption_endpoint(request: Request):
    rate_limit_service: RateLimitService = ServiceAccessor().get(RateLimitService)
    decryption_service: DecryptingService = ServiceAccessor().get(DecryptingService)
    if not rate_limit_service.get_tracked_user(request.META["REMOTE_ADDR"]).attempt():
        return Response(
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )
    algo_param = request.query_params.get("algo", "base64")
    try:
        return Response(decryption_service.decrypt(request.data, algo_param))
    except Exception as err:
        return Response({"info": str(err)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def signing_endpoint(request: Request):
    rate_limit_service: RateLimitService = ServiceAccessor().get(RateLimitService)
    signing_service: SigningService = ServiceAccessor().get(SigningService)
    if not rate_limit_service.get_tracked_user(request.META["REMOTE_ADDR"]).attempt():
        return Response(
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )
    try:
        return Response(signing_service.sign(request.data))
    except Exception as err:
        return Response({"info": str(err)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def verification_endpoint(request: Request):
    # WIP
    return Response({"info": "Field to vertify data"})
