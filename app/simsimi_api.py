from app.debug import debug
import queue
import requests

class simsimi_api:
    #여기 좀 별로인 것 같음
    #이 부분 수정
    key_list=['d587ec90-cd1b-4d59-854a-b8afad044dad',
            '66c27587-5a16-4920-94ef-fc97de7e53c8',
            '54fc844e-c898-471e-b3c1-35dd8fd9609a'
            ]
    keyQueue = queue.Queue(len(key_list))
    for idx in range(len(key_list)):
        keyQueue.put(key_list[idx])

    values={'key' : keyQueue.get(), 'lc' : 'ko', 'ft' : '1.0', 'text' : 'your TEXT HERE' }
    debug.get_instance().wlog(values)
    def get_response(text):
        # query = 'http://sandbox.api.simsimi.com/request.p?key=' + key + '&lc=en&ft=1.0&text='
        api_request_url='http://sandbox.api.simsimi.com/request.p'

        simsimi_api.values['text']=text

        url = api_request_url + '?' + 'key=' + simsimi_api.values['key'] + '&lc=en&ft=1.0&text=' + text.replace('\n','')
        #requests.get의 params 인자로 쿼리스트링 만들면 무슨 이유인지 모르겠지만 가끔 404 에러남 ex> text = kjl
        raw_response = requests.get(url)

        debug.get_instance().wlog("raw response: ")
        debug.get_instance().wlog(raw_response)

        print(raw_response.json())
        response=raw_response.json().get('response')

        debug.get_instance().wlog("response: ")
        debug.get_instance().wlog(response)

        if raw_response.json().get('result') == 100:

            response=raw_response.json().get('response')

        elif raw_response.json().get('result') == 404:

            response = "I don't know what to say!"

        elif raw_response.json().get('result') == 509:

            response = "Daily Request Limit"

        return response

    def get_key_queue():
        return simsimi_api.keyQueue
    def is_key_queue_empty():
        return simsimi_api.keyQueue.empty()
    def set_new_key():
        new_key=simsimi_api.keyQueue.get()
        simsimi_api.values['key']=new_key

        return new_key
