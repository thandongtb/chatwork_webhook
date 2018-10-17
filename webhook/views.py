from django.shortcuts import render
import hashlib
import hmac
from chatbot.chatbot_helpers import get_chatbot_response, handle_response_code
from chatbot.chatwork_helpers import Chatwork
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

def handle_payload(payload):
    if payload['webhook_event_type'] == 'mention_to_me':
        message_body = payload['webhook_event']['body'].split('\n')[-1]
        message_chatbot = get_chatbot_response(message_body)
        message_chatbot = handle_response_code(str(message_chatbot))
        message_reply_chatwork = Chatwork().get_reply_message(
            account_id=int(payload['webhook_event']['from_account_id']),
            room_id=int(payload['webhook_event']['room_id']),
            message_id=int(payload['webhook_event']['message_id']),
            message=message_chatbot
        )
        Chatwork().send_message(room_id=payload['webhook_event']['room_id'], msg=message_reply_chatwork)


@csrf_exempt
def handle_chatwork_webhook(request):
    if validate_request(request) == 0:
        return HttpResponseForbidden('Invalid signature header')
    payload = decode_payload(request)
    handle_payload(payload)
    return HttpResponse('Webhook received', status=200)