from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('YiYi')

# Get a response to an input statement
while True:
    print(chatbot.get_response(input(">")))