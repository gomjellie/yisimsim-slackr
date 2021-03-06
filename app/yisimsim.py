from app.slackbot import slackbot
from app.debug import debug
from app.simsimi_api import simsimi_api
from app.bus_api import bus_api
from app.subway_api import subway_api
from app.msg_parser import msg_parser
from app.activated_id import ActivatedID
from app.translator import translator
import sqlite3
import random
import re

class yisimsim(slackbot):

    def __init__(self, token, bot_id, google_token, read_delay):
        super(yisimsim,self).__init__(token, bot_id, read_delay)
        self._translator = translator(google_token)
        self.con = sqlite3.connect("chat.db")
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.commit()
        self.con.close()
    def run(self):
        if self.is_rtm_connected():
            debug.get_instance().wlog("yisimsim connected and running!")
            while True:
                self.fetch_msg()
                rtm_msg_list=self.get_msg()

                (text, channel, user, msg_type)=msg_parser.parse_mandatory_from(rtm_msg_list,self.AT_BOT)

                if msg_type == "command":
                    self.handle_command(text, channel, user)
                elif msg_type == "chat":
                    self.handle_chat(text, channel, user)
                else:
                    pass
        else:
            debug.get_instance().wlog("Connection failed. Invalid Slack token or bot ID?")
    #rename m's
    def handle_command(self, text, channel, user):
        #JUNK is for 쓰레기 구별
        JUNK='\"\"'
        response=None

        #/(command - only english) (args wrapped with quotes)
        pattern=r'/(?P<command>[a-zA-Z]+)\s*(?P<args>.*)'

        #text+JUNK => to always make m not None
        #example (@yisimsim /activate) > command : activate, args : ""
        m=re.match(pattern, text+JUNK)
        command=m.group('command')

        if command == "teach" or command == "delete":
            #args must be "(any character)"(at least one space)"(any character)"""
            #last two quote is JUNK
            pattern=r"\"(?P<arg0>.*)\"\s+\"(?P<arg1>.*)\"\"\""
            m2=re.match(pattern,m.group('args'))

            if m2 is not None:
                if command == "teach":
                    self.teach(m2.group('arg0'), m2.group('arg1'), user)
                    response='Q: ' + m2.group('arg0') + ' A: ' + m2.group('arg1') + ' Added to chatlog.db'
                elif command == "delete":
                    debug.get_instance().wlog("delete")
                    self.delete(m2.group('arg0'), m2.group('arg1'), user)
                    response= 'Q: ' + m2.group('arg0')+' A: ' +m2.group('arg1')+' Deleted from chatlog.db'
		
        elif command == "translate":
			
            target_pattern = r'--target\s+(?P<target>.*)\s+\"(?P<arg0>.*)\"\"\"'
            lang_pattern = r"--lang\"\""

            m1 = re.match(target_pattern, m.group('args'))

            if m1 is not None: 
				
				#set which language to translate to
                if m1.group('target') != '':
                    target = m1.group('target')
                else:
                    target = 'en'

                wannabe_translated = m1.group('arg0')
                response = self._translator.translate(wannabe_translated, target)
            else:
                m1 = re.match(lang_pattern, m.group('args'))
             
                if m1 is not None:
                    response = self._translator.availables() 
                else:
                    response = "wrong use of translate command"

        elif command == "bus":

            #args must be "(number)"""
            #last two quote is JUNK
            pattern=r'\"(?P<arg0>\d*)\"\"\"'
            m1 = re.match(pattern, m.group('args'))

            if m1 is not None:
                if command == 'bus':
                    stnNumber = int(m1.group('arg0'))
                    print(stnNumber)
                    response = bus_api.get_station_stat(stnNumber)
            else:
                response = "존재하지 않는 역입니다"

        elif command == "subway":
            #args are korean
            print(m.group('args'))
            pattern = r'\"(?P<arg0>[가-힣]*)역\"\"\"'
            m1 = re.match(pattern, m.group('args'))

            if m1 is not None:
                stnNm = str(m1.group('arg0'))
                print (stnNm)
                response = subway_api.get_station_stat(stnNm)
            else:
                response = "존재하지 않는 역입니다"

        elif command == "activate" or command == "deactivate" or command == "help":
            if m.group('args') == JUNK:
                debug.get_instance().wlog("args is JUNK")
                if command == "activate":
                    ActivatedID.get_instance().activate(user)
                    response="you've activated"
                elif command == "deactivate":
                    ActivatedID.get_instance().deactivate(user)
                    response="you've deactivated"
                elif command == "help":
                    response = "click the link for help :+1: " + "https://karlin13.github.io"
        else:
            response="틀린 형식의 명령입니다"

        self.post_msg(channel, response)
    #여기 별로인 것 같음
    def handle_chat(self, quest, channel, user):
        response=self.get_ans(quest)

        if response is None:
            response=simsimi_api.get_response(quest)

            # change until valid key pops
            while response == "Daily Request Limit":

                debug.get_instance().wlog(response)

                if simsimi_api.is_key_queue_empty():

                    response="queue is empty"
                    debug.get_instance().wlog(response)
                    break

                else:

                    debug.get_instance().wlog(simsimi_api.set_new_key())
                    response=simsimi_api.get_response(quest)
            # 404 뜨면 response가 I don't know what to say 이므로 self.teach 뺀다.
            if response != "I don't know what to say!":
                self.teach(quest, response ,user)
        self.post_msg(channel,"<@"+user+"> "+response)
        """
        self.post_msg이거 인덴트 하나 더주면 안됨
        db에 이미 있는거 질문하면 대답안하고 멈춤

        """


    def teach(self, quest, ans, user):
        self.cursor.execute("INSERT INTO chatlog VALUES (?,?,?)", (quest, ans, user))
    def delete(self, quest, ans, user):
        self.cursor.execute("DELETE FROM chatlog WHERE Quest = ? AND Ans = ? ", (quest,ans))
    def get_ans(self, quest):
        response=None

        self.cursor.execute("SELECT * FROM chatlog WHERE Quest=? ORDER BY RANDOM() LIMIT 1", (quest,))
        response_list=self.cursor.fetchone()
        print(response_list)

        if response_list is not None:
        # response=response_list[1]
        # db에서 가져온 response 쓸 확률 높임
            response = random.choice([response_list[1], response_list[1],simsimi_api.get_response(quest)])

        return response

