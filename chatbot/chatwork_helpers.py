import requests
import json
from chatwork_webhook.settings import CHATWORK_API_TOKEN

class Chatwork(object):
    # Token Header key
    TOKEN_HEADER_KEY = "X-ChatWorkToken"

    def __init__(self):
        self.apiToken = CHATWORK_API_TOKEN
        self.reqHeader = {Chatwork.TOKEN_HEADER_KEY: self.apiToken}

    def send_message(self, room_id, msg):
        uri = "https://api.chatwork.com/v2/rooms/" + str(room_id) + "/messages"
        data = {"body": msg}
        req = requests.post(uri, headers=self.reqHeader, data=data)
        return json.loads(req.text)

    def get_reply_message(self, account_id, room_id, message_id, message):
        return "[rp aid={%ld} to={%ld}-{%ld}]\n%s" % (account_id, room_id, message_id, message)
