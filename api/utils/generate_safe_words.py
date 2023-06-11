import requests
import json


def generate_safe_words():
    """
    Generates a list of 10 words from the api random word used by the company to reset the password.
    :return: list of 10 words in json.
    """
    api_url = "https://random-word-api.vercel.app/api?words=10&length=7"
    response = requests.get(api_url)
    if response.status_code != requests.codes.ok:
        return
    json_response = json.loads(response.text)
    return json_response


def make_dictio(json_response):
    """
    Converts a list of words into a dictionary, where each word is assigned its own key
    :param json_response: a list of 10 words in json.
    :return: converted list of words to a dictionary.
    """
    dictio = {}
    for index, word in enumerate(json_response, start=1):
        key = "word" + str(index)
        dictio[key] = word
    return dictio
