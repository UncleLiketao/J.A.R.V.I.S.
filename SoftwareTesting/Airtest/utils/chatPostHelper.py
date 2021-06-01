import os
import json
import requests
from .Helper import Helper

class chatPostHelper():
    def PostToIGGChat(title, message, target, targetId):
        token = os.environ.get('IGG_CHAT_TOKEN')
        if not token:
            return

        data = {
            'token': token,
            'title': title,
            'content': message,
            'content_type': 1,
            'target' : target
        }

        if target == 'group':
            data['room'] = targetId
        else:
            data['account'] = targetId

        try:
            igg_chat_url = Helper.GetSettingData()["igg_chat_url"]
            response = requests.post(igg_chat_url, json=data)
            retData = json.loads(response.text)
        except Exception as e:
            print(e)

    def PostToIGGChatGroup(target, title, message):
        chatPostHelper.PostToIGGChat(title, message, 'group', target)

    @staticmethod
    def PostToIGGSingle(target, title, message):
        chatPostHelper.PostToIGGChat(title, message, 'single', target)

    @staticmethod
    def PostMessageChannel(reportMsg, channel, title):
        chatPostHelper.PostToIGGChatGroup(channel, title, reportMsg)