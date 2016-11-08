from slackclient import SlackClient

class slackbot:
    def __init__(self,token, bot_id, read_delay):
        #self.bot_id=str()
        #hmm
        READ_WEBSOCKET_DELAY=read_delay
        self.AT_BOT="<@"+bot_id+">"
        self.sc=SlackClient(token)
        self.msg=str()
    def is_rtm_connected(self):
        return self.sc.rtm_connect()
    def post_msg(self, channel, text, as_user=True):
        self.sc.api_call("chat.postMessage", channel=channel, text=text, as_user=as_user)
    def fetch_msg(self):
        self.msg=self.sc.rtm_read()
    def get_msg(self):
        return self.msg

