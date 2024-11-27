from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.serializers import CharField, JSONField, DictField
import base64
import json
from .services.verifying import VerifyFormSerializer, VerifyForm, VerifyingService

from .services.decrypting import DecryptingService
from .services.encrypting import EncryptingService
from .services.signing import SigningService
from .utils import ServiceAccessor

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
    inline_serializer,
)

ServiceAccessor().register(DecryptingService).register(EncryptingService).register(
    SigningService
).register(VerifyingService)


import logging
logger = logging.getLogger(__name__)

@extend_schema(
    description="Encryption endpoint, can encrypt the data in entry depending of the algorithm selected (by default base64). The data in input are traversed with a depth of one",
    methods=["POST"],
    parameters=[
        OpenApiParameter(
            name="algo",
            default="base64",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Specified the algorithms used for encryption",
        )
    ],
    request=dict,
    responses={
        200: dict,
        400: dict,
    },
)

@api_view(["POST"])
def encryption_endpoint(request: Request):
    logger.debug("Received POST request on /encrypt/")
    encryption_service: EncryptingService = ServiceAccessor().get(EncryptingService)
    algo_param = request.query_params.get("algo", "base64")
    try:
        return Response(encryption_service.encrypt(request.data, algo_param))
    except Exception as err:
        return Response({"info": str(err)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="Decryption endpoint, can decrypt the data in entry depending of the algorithm selected (by default base64)",
    methods=["POST"],
    parameters=[
        OpenApiParameter(
            name="algo",
            default="base64",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Specified the algorithms used for encryption",
        )
    ],
    request=dict,
    responses={200: dict, 400: dict},
)
@api_view(["post"])
def decryption_endpoint(request: Request):
    decryption_service: DecryptingService = ServiceAccessor().get(DecryptingService)
    algo_param = request.query_params.get("algo", "base64")
    try:
        return Response(decryption_service.decrypt(request.data, algo_param))
    except Exception as err:
        return Response({"info": str(err)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="Signing endpoint, return the signature hash for the data in input",
    methods=["POST"],
    request=str,
    responses={
        200: str,
        400: dict,
    },
)
@api_view(["POST"])
def signing_endpoint(request: Request):
    signing_service: SigningService = ServiceAccessor().get(SigningService)
    try:
        return Response(signing_service.sign(request.data))
    except Exception as err:
        return Response({"info": str(err)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="verifying endpoint, check the data in entry match the hash signature. Emit an 204 status if it is unmatched",
    methods=["POST"],
    request=VerifyFormSerializer,
    responses={
        200: dict,
        204: None,
        400: dict,
    },
)
@extend_schema(request=VerifyFormSerializer)
@api_view(["POST"])
def verification_endpoint(request: Request):
    verifying_service: VerifyingService = ServiceAccessor().get(VerifyingService)
    serializer = VerifyFormSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            "The verify form send in entry is not correct",
            status=status.HTTP_400_BAD_REQUEST,
        )
    verify_form = VerifyForm(**serializer.validated_data)
    try:
        if verifying_service.verify(verify_form):
            return Response({"info": "The signature is valid"})
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as err:
        return Response({"info": str(err)}, status=status.HTTP_400_BAD_REQUEST)
