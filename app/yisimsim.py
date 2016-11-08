from app.slackbot import slackbot
from app.debug import debug
from app.simsimi_api import simsimi_api
from app.msg_parser import msg_parser
from app.activated_id import ActivatedID
import sqlite3
import re

class yisimsim(slackbot):

    def __init__(self, token, bot_id, read_delay):
        super(yisimsim,self).__init__(token, bot_id, read_delay)
        self.con = sqlite3.connect("chat.db")
        self.cursor = self.con.cursor()
        self.simsimi=simsimi_api()

    def __del__(self):
        self.con.commit()
        self.con.close()
    def run(self):
        if self.is_rtm_connected():
            debug.wlog("yisimsim connected and running!")
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
            debug.wlog("Connection failed. Invalid Slack token or bot ID?")
    #rename m's
    def handle_command(self, text, channel, user):
        #JUNK is for 쓰레기 구별
        JUNK='\"\"'
        response=None

        pattern=r'/(?P<command>[a-zA-Z]+)\s*(?P<args>\".*\")'

        #text+JUNK => to always make m0 not None
        m0=re.match(pattern, text+JUNK)

        command=m0.group('command')

        if command == "teach" or command == "delete":
            pattern=r"\"(?P<arg0>.*)\"\s+\"(?P<arg1>.*)\"\"\""
            m1=re.match(pattern,m0.group('args'))

            if m1 is not None:
                if command == "teach":
                    self.teach(m1.group('arg0'), m1.group('arg1'), user)
                    response='Q: ' + m1.group('arg0') + ' A: ' + m1.group('arg1') + ' Added to chatlog.db'
                elif command == "delete":
                    debug.wlog("delete")
                    self.delete(m1.group('arg0'), m1.group('arg1'), user)
                    response= 'Q: ' + m1.group('arg0')+' A: ' +m1.group('arg1')+' Deleted from chatlog.db'
        elif command == "activate" or command == "deactivate":
            if m0.group('args') == JUNK:
                debug.wlog("args is JUNK")
                if command == "activate":
                    ActivatedID.activate(user)
                    response="you've activated"
                elif command == "deactivate":
                    ActivatedID.deactivate(user)
                    response="you've deactivated"
        else:
            response="틀린 형식의 명령입니다"

        self.post_msg(channel, response)
    #여기 별로인 것 같음
    def handle_chat(self, quest, channel, user):
        response=self.get_ans(quest)

        if response is None:
            response=self.simsimi.get_response(quest)

            if response is None:
                response="daily query limit"
                debug.wlog(response)
                if self.simsimi.is_key_queue_empty():
                    response="queue is empty"
                    debug.wlog(response)
                else:
                    debug.wlog(self.simsimi.set_new_key())
                    response=self.simsimi.get_response(quest)
            self.teach(quest, response ,user)
            self.post_msg(channel,"<@"+user+"> "+response)



    def teach(self, quest, ans, user):
        self.cursor.execute("INSERT INTO chatlog VALUES (?,?,?)", (quest, ans, user))
    def delete(self, quest, ans, user):
        self.cursor.execute("DELETE FROM chatlog WHERE Quest = ? AND Ans = ? ", (quest,ans))
    def get_ans(self, quest):
        response=None

        self.cursor.execute("SELECT * FROM chatlog WHERE Quest=? ORDER BY RANDOM() LIMIT 1", (quest,))
        response_list=self.cursor.fetchone()

        if response_list is not None:
            response=response_list[1]

        return response

