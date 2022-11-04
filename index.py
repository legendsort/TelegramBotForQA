from flask import Flask
from flask import request
from flask import Response
import requests
import json

TOKEN = "5773306905:AAFmcc0xlg5B6Sut6lAM39LF6J5uhYZhA5U"
menu = 1
activity = 1
language = 0

app = Flask(__name__)

with open("./env", "r") as file:
    TOKEN = json.load(file)
    
with open("./botStep.json", "r") as file:
    botStep = json.load(file)

def parse_message(message):
    try:
        if 'message' in message:
            chat_id = message['message']['chat']['id']
            txt = message['message']['text']
            return chat_id,txt,""
        elif 'callback_query' in message:
            chat_id = message['callback_query']['message']['chat']['id']
            txt = message['callback_query']['data']
            quiz = message['callback_query']['message']['text']
            
            return chat_id,txt,quiz
        return -1, -1, -1
    except:
        print("Something wrong")
        return -1, -1, -1

def tel_send_message(chat_id, text):
    url = 'https://api.telegram.org/bot5773306905:AAFmcc0xlg5B6Sut6lAM39LF6J5uhYZhA5U/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }  
    r = requests.post(url,json=payload)
    return r

def tel_send_inlinebutton(chat_id, text, options):
    url = 'https://api.telegram.org/bot5773306905:AAFmcc0xlg5B6Sut6lAM39LF6J5uhYZhA5U/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': {
            "inline_keyboard": options
        }
    }
    r = requests.post(url, json=payload)
    return r

def arrayToMarkup(arr, multi):
    ans = []
    num = 0
    for index, item in enumerate(arr):
        if multi == False:
            ans.append({
                "text": item,
                "callback_data": index,
            })
        else:
            temp = []
            for it in item:
                temp.append({
                    "text": it,
                    "callback_data": num,
                })
                num += 1
            
            ans.append(temp)
        pass
    if multi == False: ans = [ans]
    return ans


def inlineButton(chatID, item):
    option = item['option']
    markUp = arrayToMarkup(option, True if 'multi' in item else False)
    tel_send_inlinebutton(chatID, item['text'], markUp)
    return ""


def sendMessage(chatID, item):
    text = item['text']
    tel_send_message(chatID, text)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global activity, menu, language

        msg = request.get_json()
        chat_id, txt, quiz = parse_message(msg)
        if chat_id == -1:
            return Response('bad', status=200)
        item = {}
        if txt == '/start':
            item = botStep["Language Option"][language]
        if quiz == 'Please choose your preferred language:':
            language = int(txt)
            item = botStep["Activity Selection"][language]

        if quiz == 'Sila Pilih Aktiviti' or quiz == 'Choose Activity':
            activity = int(txt)
            if(activity == 0): 
                item = botStep['Sub Activity Selection'][language]
            else:
                item = botStep['Main Menu'][language]

        if quiz == 'Sila Pilih Sub Aktiviti' or quiz == 'Please Select Sub Activity':
            activity = 3 + int(txt)
            item = botStep['Main Menu'][language]

        if quiz == 'Sila Pilih Maklumat Yang Diperlukan' or quiz == 'Please Select the Required Information':
            menu = int(txt)
            key = "Option %s-%s" % (activity + 1, menu+1)
            item = botStep[key][language]
        
        if 'type' not in item:
            tel_send_message(chat_id, 'Wrong Command')
            return Response('bad', status=200)
        
        if item['type'] == 'InlineButton':
            inlineButton(chat_id, item)
        if item['type'] == 'text':
            sendMessage(chat_id, item)

        return Response('ok', status=200)
 
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
