import sys
import requests


'''

    ЗАПУСК: python3 main.py <путь к файлу в формате ogg>
    ПРИМЕР: python3 main.py ./static/test2.ogg

    TODO: 
    2 - печатать результат скрипта в отдельный файл (а потом скрипт с андроид-приложением будут общаться через сокеты)
    3 - менять Content-Type автоматически в зависимости от формата файла

'''


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

with open(sys.argv[1], 'rb') as f:
    data = f.read()

response = requests.post('https://smartspeech.sber.ru/rest/v1/speech:recognize', headers=headers, data=data, verify=certificate_path)

# вывод результата
print(response.status_code)
print(response.json()['result'])
