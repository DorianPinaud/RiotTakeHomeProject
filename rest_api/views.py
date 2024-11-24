from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
import base64
import json
from .rate_limit_service import (
    RateLimitService,
    RateLimitTracker,
    TimeRateLimitTrackerFactory,
)
from .utils import ServiceAccessor

ServiceAccessor().register(
    RateLimitService,
    [
        TimeRateLimitTrackerFactory(max_limit_in_second=1, max_usage_per_second=60),
    ],
)


@api_view(["POST"])
def encryption_endpoint(request: Request):
    rate_limit_service: RateLimitService = ServiceAccessor().get_service(
        RateLimitService
    )
    if not rate_limit_service.get_tracked_user(request.META["REMOTE_ADDR"]).attempt():
        return Response(
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    ret = {}
    for key, value in request.data.items():
        text = json.dumps(value)
        text_bytes = text.encode("ascii")
        base64_byte = base64.b64encode(text_bytes)
        base64_text = base64_byte.decode("ascii")
        ret[key] = base64_text

    return Response(ret)


@api_view(["post"])
def decryption_endpoint(request: Request):
    rate_limit_service: RateLimitService = ServiceAccessor().get_service(
        RateLimitService
    )
    if not rate_limit_service.get_tracked_user(request.META["REMOTE_ADDR"]).attempt():
        return Response(
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    ret = {}
    for key, value in request.data.items():
        base64_byte = value.encode("ascii")
        text_byte = base64.b64decode(base64_byte)
        text = text_byte.decode("ascii")
        data = json.loads(text)
        ret[key] = data

    return Response(ret)


@api_view(["GET"])
def getSignature(request: Request):
    # WIP
    return Response({"info": "Field to sign data"})


@api_view(["GET"])
def getVerification(request: Request):
    # WIP
    return Response({"info": "Field to vertify data"})
