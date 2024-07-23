from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse

import os
import requests

app = FastAPI()

'''
    ПЕРЕД ЗАПУСКОМ:
        1) Открыть терминал в папке проекта (где лежит main.py)
        2) mkdir ./statiс
        3) В директорию /static поместить файлы AuthData.txt и RqUID.txt, в которых, соответственно, находятся значения Авторизационного ключа и RqUID
        4) В ту же директрию поместить файл сертификата Минцифры russiantrustedca.pem
        5) Устанавливаем пайтоновские зависимости через pip install -r requirements.txt
        6) mkdir ./audios
 
    ЗАПУСК: uvicorn main:app --host 0.0.0.0 --port 8000

    ---------------------------------------------------

    TODO на 24.07:
    1) прикрутить нейросеть

'''


def speech_to_text(filepath):
    # получаем необходимые данные из других файлов
    certificate_path = "static/russiantrustedca.pem"

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

        text = speech_to_text(filepath)
        os.remove(filepath)

        return text