from app.debug import debug
import queue
import requests

class simsimi_api:
    #여기 좀 별로인 것 같음
    #이 부분 수정
    key_list=['037def59-fda0-46eb-93f4-9fce096f3528','b1447f3f-1907-42a2-a9c7-c7b91af21363']
    keyQueue = queue.Queue(len(key_list))
    for idx in range(len(key_list)):
        keyQueue.put(key_list[idx])

    values={'key' : keyQueue.get(), 'lc' : 'ko', 'ft' : '1.0', 'text' : 'your TEXT HERE' }
    debug.wlog(values)
    def get_response(text):
        # query = 'http://sandbox.api.simsimi.com/request.p?key=' + key + '&lc=en&ft=1.0&text='
        api_request_url='http://sandbox.api.simsimi.com/request.p'

        simsimi_api.values['text']=text

        raw_response=requests.get(api_request_url,params=simsimi_api.values)

        debug.wlog("raw response: ")
        debug.wlog(raw_response)

        response=raw_response.json().get('response')

        debug.wlog("response: ")
        debug.wlog(response)

        return response

    def get_key_queue():
        return simsimi_api.keyQueue
    def is_key_queue_empty():
        return simsimi_api.keyQueue.empty()
    def set_new_key():
        new_key=simsimi_api.keyQueue.get()
        simsimi_api.values['key']=new_key

        return new_key
