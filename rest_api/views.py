from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
import base64
import json
from collections import defaultdict
import time

nbr_request_by_client = defaultdict(lambda: {"counter": 0, "time": time.time()})
max_request_per_second = 60


@api_view(["POST"])
def encryption_endpoint(request: Request):
    client_remote_address = request.META["REMOTE_ADDR"]

    if (time.time() - nbr_request_by_client[client_remote_address]["time"]) > 1:
        nbr_request_by_client[client_remote_address]["time"] = time.time()
        nbr_request_by_client[client_remote_address]["counter"] = 0

    nbr_request_by_client[client_remote_address]["counter"] += 1

    if nbr_request_by_client[client_remote_address]["counter"] > max_request_per_second:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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
    client_remote_address = request.META["REMOTE_ADDR"]

    if (time.time() - nbr_request_by_client[client_remote_address]["time"]) > 1:
        nbr_request_by_client[client_remote_address]["time"] = time.time()
        nbr_request_by_client[client_remote_address]["counter"] = 0

    nbr_request_by_client[client_remote_address]["counter"] += 1

    if nbr_request_by_client[client_remote_address]["counter"] > max_request_per_second:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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
