from app.debug import debug
import queue
import requests

class simsimi_api:
    #여기 좀 별로인 것 같음
    def __init__(self):
        #이 부분 수정
        self.key_list=['037def59-fda0-46eb-93f4-9fce096f3528','b1447f3f-1907-42a2-a9c7-c7b91af21363']
        self.keyQueue = queue.Queue(len(self.key_list))
        for idx in range(len(self.key_list)):
            self.keyQueue.put(self.key_list[idx])

        self.values={'key' : self.keyQueue.get(), 'lc' : 'ko', 'ft' : '1.0', 'text' : 'your TEXT HERE' }
        debug.wlog(self.values)
    def get_response(self,text):
        # query = 'http://sandbox.api.simsimi.com/request.p?key=' + key + '&lc=en&ft=1.0&text='
        api_request_url='http://sandbox.api.simsimi.com/request.p'

        self.values['text']=text

        #raw_response=requests.get(api_request_url,params=self.values)
        raw_response=requests.get("http://sandbox.api.simsimi.com/request.p?key=b1447f3f-1907-42a2-a9c7-c7b91af21363&lc=en&ft=1.0&text="+text)
        debug.wlog("raw response: ")
        debug.wlog(raw_response)
        response=raw_response.json().get('response')
        debug.wlog("response: ")
        debug.wlog(response)
        return response

    def get_key_queue(self):
        return self.keyQueue
    def is_key_queue_empty(self):
        return self.keyQueue.empty()
    def set_new_key(self):
        new_key=self.keyQueue.get()
        self.values['key']=new_key

        return new_key
