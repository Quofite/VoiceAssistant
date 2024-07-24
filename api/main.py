from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse

import os
import json
import requests

app = FastAPI()
certificate_path = "static/russiantrustedca.pem"

'''
    ПЕРЕД ЗАПУСКОМ:
        1) Открыть терминал в папке проекта (где лежит main.py)
        2) mkdir ./statiс
        3) В директорию /static поместить файлы AuthData.txt, AuthDataAI.txt и RqUID.txt, в которых, соответственно, находятся значения Авторизационного ключа STT, GigaChatAPI и RqUID
        4) В ту же директрию поместить файл сертификата Минцифры russiantrustedca.pem
        5) Устанавливаем пайтоновские зависимости через pip install -r requirements.txt
        6) mkdir ./audios
 
    ЗАПУСК: uvicorn main:app --host 0.0.0.0 --port 8000

    ---------------------------------------------------

    TODO:
    1) Прикрутить Text-To-Speech
    2) Улучшить дизайн Андроид-приложения
    3) Улучшить производительность Андроид-приложения
    4) Провести рефактор кода
'''


def speech_to_text(filepath):

    with open("./static/AuthData.txt") as ad:
        auth_data = ad.read().rstrip()

    with open("./static/RqUID.txt") as id:
        rquid = id.read().rstrip()


    # получение токена
    headers = {
        'Authorization': 'Basic ' + auth_data,
        'RqUID': rquid,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post('https://ngw.devices.sberbank.ru:9443/api/v2/oauth', headers=headers, data= {'scope': 'SALUTE_SPEECH_PERS'}, verify=certificate_path)
    access_token = response.json()['access_token']


    # запрос к апишке сбербанка
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'audio/ogg;codecs=opus'
    }

    with open(filepath, 'rb') as f:
        data = f.read()

    response = requests.post('https://smartspeech.sber.ru/rest/v1/speech:recognize', headers=headers, data=data, verify=certificate_path)

    return response.json()['result']


# --------- Метод с отетом нейросетки
def ai_response(text):
    with open("./static/AuthDataAI.txt") as ad:
        auth_data = ad.read().rstrip()

    with open("./static/RqUID.txt") as id:
        rquid = id.read().rstrip()


    # получение токена
    headers = {
        'Authorization': 'Basic ' + auth_data,
        'RqUID': rquid,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': "application/json"
    }

    response = requests.post('https://ngw.devices.sberbank.ru:9443/api/v2/oauth', headers=headers, data= {'scope': 'GIGACHAT_API_PERS'}, verify=certificate_path)
    access_token = response.json()['access_token']

    # запрос к нейросетке  
    data = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ],
        "n": 1,
        "max_tokens": 210,
        "stream": False,
        "repetition_penalty": 1
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.post('https://gigachat.devices.sberbank.ru/api/v1/chat/completions', headers=headers, data=data, verify=certificate_path)

    return response.json()['choices'][0]['message']['content']


# ------------------ HTTP HANDLERS
@app.get("/")
def read_root():
    return HTMLResponse(content="test")


@app.post("/upload")
async def upload_file(file: UploadFile | None = None):

    if not file:
        return {"message": "no file"}
    
    else:
        filepath = "./audios/" + file.filename

        with open(filepath, 'wb') as f:
            f.write(file.file.read())

        ai_answer = ai_response(speech_to_text(filepath)[0])
        os.remove(filepath)

        return ai_answer
    