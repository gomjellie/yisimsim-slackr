import requests

values = {
    'key':'037def59-fda0-46eb-93f4-9fce096f3528',
    'lc': 'en',
    'ft': '1.0',
    'text': 'your TEXT HERE'
}

key = '037def59-fda0-46eb-93f4-9fce096f3528'
query = 'http://sandbox.api.simsimi.com/request.p?key=' + key + '&lc=en&ft=1.0&text='
url = 'http://sandbox.api.simsimi.com/request.p'

r= requests.get(query + 'do you know kimchi?')
values['text'] = '뭐해?'
r = requests.get(url, params = values)
print(r.json()['response'])
