from chatterbot import ChatBot
from chatwork_webhook.settings import CHATBOT_DATABASE

def get_chatbot_response(message):
    chatbot = ChatBot(
        "Chatwork Bot",
        database=CHATBOT_DATABASE,
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': 0.6,
                'default_response': [
                    "(githe2) em bó tay",
                    "(caigithe2) hỏi khó quá",
                    "(lay3) cái này em không biết",
                    "(leuleu2) em chịu thôi",
                ]
            },
        ],
    )
    return chatbot.get_response(message)