import os
import json
from html.parser import HTMLParser

import requests


class translator:
    _base_url = 'https://translation.googleapis.com/language/translate/v2'
    _html_parser = HTMLParser()

    def __init__(self, api_key):
        self._api_key = api_key
        self._default_target = 'en'

    def translate(self, msg, target=None):
        if not target:
            target = self._default_target
        params = {
            'key': self._api_key,
            'target': target,
            'q': msg,
        }
        resp = requests.get(self._base_url, params=params).json()
        translated_msg = resp['data']['translations'][0]['translatedText']
        return self._unescape(translated_msg)

    def availables(self):
        params = {
            'key': self._api_key,
        }
        resp = requests.get(self._base_url + '/languages', params=params).json()
        langs = [lang['language'] for lang in resp['data']['languages']]
        info = '사용 가능한 언어 코드는 다음과 같아요 ^ㅇ^\n\n'
        return info + ', '.join(langs)

    def set_default_target(self, target):
        self._default_target = target

    def _unescape(self, msg):
        return self._html_parser.unescape(msg)


