import time

import requests
import json

def delete():
    while True:
        import chat_Bot
        # key = json.dumps(chat_Bot.dict_id_worker1[message.from_user.id])
        # second = {'json_s': key}
        # clientnumber = requests.post("http://api.ipstack.com/check?access_key=7bf909a062d917570aabe976dfeffa9e")
        clientnumber = requests.get("http://178.154.213.228:8000/api/smartquerest/get_moved_guests/")
        temp = json.loads(clientnumber.json())
        if not temp['empty']:
            # print(12)
            # print(a)
            chat_Bot.notify_all(temp['guests'])
        # print(temp)
        # print(type(temp))
        time.sleep(1)
