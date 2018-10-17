from chatterbot import ChatBot
from chatwork_webhook.settings import CHATBOT_DATABASE
import random
from chatbot.doodle_helpers import get_weekday_calendar

chatbot = ChatBot(
    "Chatwork Bot",
    database=CHATBOT_DATABASE,
    read_only = True,
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.5,
            'default_response': "default_response"
        },
    ],
)

def get_chatbot_response(message):
    response =  chatbot.get_response(message)
    if response == 'default_response':
        response = random.choice([
                "(githe2) em bó tay",
                "(caigithe2) hỏi khó quá",
                "(lay3) cái này em không biết",
                "(leuleu2) em chịu thôi",
            ])
    return response

def handle_response_code(message):
    if '_work_schedule' in message:
        weekday_name = message.split('_work_schedule')[0]
        message = get_weekday_calendar(weekday_name)
    return message