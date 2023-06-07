import requests
import json


def generate_safe_words():

    api_url = "https://random-word-api.vercel.app/api?words=10&length=7"
    response = requests.get(api_url)
    if response.status_code != requests.codes.ok:
        return
    json_response = json.loads(response.text)
    return json_response


def make_dictio(json_response):
    dictio = {}
    for index, word in enumerate(json_response, start=1):
        key = "word" + str(index)
        dictio[key] = word
    return dictio
