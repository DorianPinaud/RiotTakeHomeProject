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

from .encoder_service import OneDepthEncoder, EncoderStrategyFactory
from .decoder_service import OneDepthDecoder, Base64DecodingStrategy
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

    encoder = OneDepthEncoder()

    return Response(
        encoder.encode(request.data, EncoderStrategyFactory().create_strategy())
    )


@api_view(["post"])
def decryption_endpoint(request: Request):
    rate_limit_service: RateLimitService = ServiceAccessor().get_service(
        RateLimitService
    )
    if not rate_limit_service.get_tracked_user(request.META["REMOTE_ADDR"]).attempt():
        return Response(
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    decoder = OneDepthDecoder()
    return Response(decoder.decode(request.data, Base64DecodingStrategy()))


@api_view(["GET"])
def getSignature(request: Request):
    # WIP
    return Response({"info": "Field to sign data"})


@api_view(["GET"])
def getVerification(request: Request):
    # WIP
    return Response({"info": "Field to vertify data"})
