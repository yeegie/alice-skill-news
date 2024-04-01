# coding: utf-8
from __future__ import unicode_literals

import functions

import logging

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

def handle_dialog(request):
    utterance = request['request']['original_utterance'].lower()
    print(f'[✨] "{utterance}".')
    if utterance == 'телеграм':
        return 'Чтобы подключить телеграм, введите секретную фразу из бота, если вы не понимаете о чем речь скажите "помощь", чтобы отменить подключение "отмена".'
    elif utterance == 'помощь':
        return 'Помощь'
    elif utterance == 'отмена':
        return 'Отмена'

@app.route('/', methods=['POST'])
def main():
    req = request.get_json(force=True)
    session = req['session']
    user_id = session['user_id']
    is_auth = functions.is_auth()

    response_text = handle_dialog(req)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'text': response_text,
            'end_session': False
        }
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
