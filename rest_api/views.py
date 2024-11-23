from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view


@api_view(["GET"])
def getEncryption(request: Request):
    # WIP
    return Response({"info": "Field to encrypt data"})


@api_view(["GET"])
def getDecryption(request: Request):
    # WIP
    return Response({"info": "Field to decrypt data"})


@api_view(["GET"])
def getSignature(request: Request):
    # WIP
    return Response({"info": "Field to sign data"})


@api_view(["GET"])
def getVerification(request: Request):
    # WIP
    return Response({"info": "Field to vertify data"})
