import os
import time
import sqlite3
import queue
import requests
from slackclient import SlackClient

# export BOT_ID and SLACK_BOT_TOKEN
import exportSettings

# startbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
# AT_BOT = "심심아"
AT_BOT = "<@" + BOT_ID + ">"

# instant Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# prepare db stuff
con = sqlite3.connect("chat.db")
# cursor.execute("CREATE TABLE chatlog(Quest text, Ans text, Usr text)") 이 주석은 절대 지우지마

keyQueue = queue.Queue(2)
keyQueue.put('037def59-fda0-46eb-93f4-9fce096f3528')
keyQueue.put('b1447f3f-1907-42a2-a9c7-c7b91af21363')

class ActivatedID():
    activated_id = {}
    def is_activated(usr_id):
        if ActivatedID.activated_id.get(usr_id) == True:
            return True
        else:
            return False
    def activate(usr_id):
    	ActivatedID.activated_id[usr_id] = True
    def deactivate(usr_id):
    	del ActivatedID.activated_id[usr_id]

values = {
    'key': keyQueue.get(),  # '037def59-fda0-46eb-93f4-9fce096f3528',
    'lc': 'ko',  # en
    'ft': '1.0',
    'text': 'your TEXT HERE'
}

# query = 'http://sandbox.api.simsimi.com/request.p?key=' + key + '&lc=en&ft=1.0&text='
url = 'http://sandbox.api.simsimi.com/request.p'

def teach(quest, ans, usr):
    """
    quest, ans, usr required

    """
    cursor = con.cursor()
    con.execute("INSERT INTO chatlog VALUES (?,?,?)", (quest, ans, usr))
    con.commit()

def delete(quest, ans, usr):
    """
    delete Quest = quest AND Ans = ans
    doesn't consider usrData
    """
    cursor = con.cursor()
    cursor.execute("DELETE FROM chatlog WHERE Quest = ? AND Ans = ? ", (quest,ans))
    con.commit()

def get_ans(quest):
    """
    if it doesn't have profit data then returns None
    else if returns profit response

    """
    cursor = con.execute("SELECT * FROM chatlog WHERE Quest=? ORDER BY RANDOM() LIMIT 1", (quest,))
    resp = cursor.fetchone()
    if resp is None:
    	return None
    else :
    	return resp[1]

def handle_command(command, channel, user):
    """
    command must starts with / and have args braced with "

    """
    print('starts with /')
    cmd = command.split(' ')[0].split('/')[1]
    print('cmd is ' + cmd)
    if len(command.split('\"')) == 5:
        arg = command.split('\"')[1].strip().lower(), command.split('\"')[3].strip().lower() #인자가 1개 밖에 없는 상황이면 팅김
        print('arg is ' , arg)
        if cmd == 'teach':
            teach(arg[0], arg[1], user)
            ans = 'Q: ' + arg[0] + ' A: ' + arg[1] + 'Added to chatlog.db'
        elif cmd == 'delete':
            delete(arg[0], arg[1], user)
            ans = 'Q: ' + arg[0] + ' A: ' + arg[1] + 'Deleted from chatlog.db'
        else:
            ans = 'i dont know that command yet'
    elif len(command.split('\"')) == 1:
        if cmd == 'activate':
            ActivatedID.activate(user)
            ans = 'you\'ve activated'
        elif cmd == 'deactivate':
            ActivatedID.deactivate(user)
            ans = 'you\'ve de activated'
        else:
            ans = 'i dont know that command yet'
    else:
        ans = '전달인자 개수가 맞지않습니다 \nyou can get helps in --help option'

    slack_client.api_call("chat.postMessage", channel=channel, text=ans, \
            as_user=True)

def handle_chat(command, channel, user):
    """
    Receives commands directed at the bot and determines if they
    are valid commands. If so, then acts on the commands. If not,
    returns back what it needs for clarification.
    """

    values['text'] = command
    r = requests.get(url, params=values)

    ans = get_ans(command)
    if not ans:
        ans = r.json().get('response')

        if not ans:
            print("DailyQueryLimit")
            if keyQueue.empty():
                print("queue is Empty")
                ans = "queue is Empty"
            else:
                values['key'] = keyQueue.get()
                print(values['key'])
                r = requests.get(url, params=values)
                ans = r.json().get('response')

    teach(command, ans, user)
    slack_client.api_call("chat.postMessage", channel=channel, text='<@' + user + '> ' + ans, \
                          as_user=True)

def parse_slack_output(slack_rtm_output):
    """
    The Slack Real Time Messaging API is an events firehose.
    this parsing function returns None unless a message is
    directed at the Bot, based on its ID.

    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                """
                WHAT output looks like:
                this is what i got when run print(output)
                {'type': 'message', 'user': 'U1E5YRSM6', 'channel': 'C2UEKTP38', 'ts': '1477806948.000019',
                'text': '<@U2UD924JH> 안녕', 'team': 'T1960F6SW'}
                """
                return (output['text'].split(AT_BOT)[1].strip().lower(), \
                        output['channel'], output['user'])
            elif output and 'text' in output and 'user' in output and ActivatedID.is_activated(output['user']):
            	print(output)
            	return output['text'], output['channel'], output['user']
    return None, None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel and user:
                if command.startswith('/'):
                    handle_command(command, channel, user)
                else:
                    handle_chat(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
