
class yisimsim(slackbot):

    def __init(self, token, bot_id, read_delay):
        super(yisimsim,self).__init__(token, bot_id, read_delay)
        self.con = sqlite3.connect("chat.db")
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.commit()
        self.con.close()
    def run(self):
        if self.is_rtm_connected():
            debug.wlog("yisimsim connected and running!")
            while True:
                self.fetch_rtm_msg()
                rtm_msg_list=self.get_msg()

                (text, channel, user, msg_type)=msg_parser.parse_mandatory_from(rtm_msg_list,self.at_bot)

                if msg_type == "command":
                    pass
                elif msg_type == "chat":
                    pass
                else:
                    pass
        else:
            debug.wlog("Connection failed. Invalid Slack token or bot ID?")
    #rename m's
    def handle_command(self, text, channel, user):
        #JUNK is for 쓰레기 구별
        JUNK='""'
        response=None

        pattern=self.at_bot+r'\s+(?P<command>/[a-zA-Z]+)\s+(?P<args>\".*\")'
        #text+JUNK => to always make m0 not None
        m0=re.match(pattern, text+JUNK)

        command=m0.group('command')

        if command == "teach" or command == "delete":
            pattern=r"\"(?P<arg0>.*)\"\s+\"(?P<arg1>.*)\"\"\""
            m1=re.match(pattern,m0.group('args'))

            if m1 is not None:
                if command == "teach":
                    teach(m1.group('arg0'), m1.group('arg1'), user)
                    reponse='Q: ' + m1.group('arg0') + ' A: ' + m1.group('arg1') + ' Added to chatlog.db'
                elif command == "delete":
                    delete(m.group('arg0'), m.group('arg1'), user)
                    reponse= 'Q: ' + m1.group('arg0') ' A: ' +m1.group('arg1') ' Deleted from chatlog.db'
        elif command == "activate" or command == "deactivate":
            if m0.group('args') == JUNK:
                if command == "activate":
                    activated_id.activate(user)
                    response="you've activated"
                elif command == "deactivate":
                    activated_id.deactivate(user)
                    response="you've deactivated"
        else:
            response="틀린 형식의 명령입니다"

        self.post_msg(channel, response)

    def handle_chat(self):
        pass
    def teach(self, quest, ans, user):
        self.cursor.execute("INSERT INTO chatlog VALUES (?,?,?)", (quest, ans, user))
    def delete(self, quest, ans, user):
         self.cursor.execute("DELETE FROM chatlog WHERE Quest = ? AND Ans = ? ", (quest,ans))
    def get_ans(self):
        pass
