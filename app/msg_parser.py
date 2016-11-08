from app.activated_id import ActivatedID
import re

class msg_parser:
    def parse_command_from():
        pass
    def parse_qna_from():
        pass
    def parse_mandatory_from(rtm_msg_list, at_bot):
        '''
            returns text, channel, user, msg_type(is_chat? is_command?)
        '''
        (text, channel, user, msg_type)=(None, None, None, None)
        rtm_msg=None

        #rtm_msg_list -> [{1:2,2:3....}]
        #rtm_msg -> {1:2,2:3...}
        if rtm_msg_list != []:
            rtm_msg=rtm_msg_list[0]

        if rtm_msg and ('text' in rtm_msg) and ('user' in rtm_msg):
            #get channel and user
            (channel, user)=(rtm_msg['channel'], rtm_msg['user'])

            #get text
            if (at_bot in rtm_msg['text']):
                pattern = at_bot + r"\s+(?P<text>.*)"
                m=re.match(pattern, rtm_msg['text'])
                text=m.group("text")

            elif ActivatedID.is_activated(user):
                text=rtm_msg['text']

            #check msg_type (chat vs command vs none)
            if text is not None:
                if text.startswith('/'):
                    msg_type="command"
                else:
                    msg_type="chat"
        return (text, channel, user, msg_type)
