from django.shortcuts import render
import hashlib
import hmac
import http.client as client
import json
import base64

from chatwork_webhook import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def validate_request(request):
    # Check the X-Hub-Signature header to make sure this is a valid request.
    chatwork_signature = request.META['HTTP_X_CHATWORKWEBHOOKSIGNATURE']
    chatwork_signature = bytes(chatwork_signature, encoding='utf-8')
    signature = hmac.new(settings.CHATWORK_WEBHOOK_SECRET, request.body, hashlib.sha256)
    expected_signature = base64.b64encode(signature.digest())

    if not hmac.compare_digest(chatwork_signature, expected_signature):
        return 0
    return 1

def decode_payload(request):
    payload = str(request.body, encoding='utf-8')
    return json.loads(payload)

@csrf_exempt
def handle_chatwork_webhook(request):
    if validate_request(request) == 0:
        return HttpResponseForbidden('Invalid signature header')
    payload = decode_payload(request)
    event = payload['webhook_event_type']
    print(event)
    return HttpResponse('Webhook received', status=200)