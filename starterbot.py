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
EXAMPLE_COMMAND = "/"

# instant Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# prepare db stuff
con = sqlite3.connect("chat.db")
print("chat.db created !")
cursor = con.cursor()
print("cursor created !")
# cursor.execute("CREATE TABLE chatlog(Quest text, Ans text, Usr text)")
isLearning = False
prevQuest = ''

keyQueue = queue.Queue(2)
keyQueue.put('037def59-fda0-46eb-93f4-9fce096f3528')
keyQueue.put('b1447f3f-1907-42a2-a9c7-c7b91af21363')

values = {
    'key': keyQueue.get(),  # '037def59-fda0-46eb-93f4-9fce096f3528',
    'lc': 'ko',  # en
    'ft': '1.0',
    'text': 'your TEXT HERE'
}
#
# query = 'http://sandbox.api.simsimi.com/request.p?key=' + key + '&lc=en&ft=1.0&text='
url = 'http://sandbox.api.simsimi.com/request.p'
#
# r= requests.get(query + 'do you know kimchi?')
# values['text'] = '뭐해?'
r = requests.get(url, params=values)


# print(r.json()['response'])

class DailyQueryLimit(Exception):
    print("DailyQueryLimit")
    pass


def handle_command(command, channel, user):
	print('starts with /')
def handle_chat(command, channel, user):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    global isLearning
    global cursor
    global prevQuest
    values['text'] = command
    r = requests.get(url, params=values)

    #
    #    if not isLearning:
    #        print("if not isLearning")
    #        con.execute("INSERT INTO chatlog VALUES (?,?,?)", (command, 'LEARNING', user))
    #        cursor = con.execute("SELECT * FROM chatlog WHERE Quest=? ORDER BY RANDOM() LIMIT 1", (command,))
    #        response = cursor.fetchone()
    #        if not response:
    #            print("if not response")
    #
    #            prevQuest = command
    #            response = 'what can i say to ' + command + ' ?'
    #            isLearning = True
    #        else:
    #            if response[1] == 'LEARNING':
    #            	response = 'what could i response to ' + command + ' ?'
    #            	isLearning = True
    #            	prevQuest = command
    #            else :
    #                response = response[1]
    #                isLearning = False;
    #        #if command.startswith(EXAMPLE_COMMAND):
    #            #response = "뭐하라고?"
    #
    #    else: #if isLearning == True
    #    	print("isLearning == True")
    #    	t = (prevQuest, command, user)
    #    	#cursor.execute("DELETE FROM chatlog WHERE Ans=?", ('LEARNING',))
    #    	cursor.execute("INSERT INTO chatlog VALUES (?,?,?)", t)
    #    	response = "i've learned well"
    #    	isLearning = False;
    #    cursor.execute("DELETE FROM chatlog WHERE Ans=?", ('LEARNING',))
    #    con.commit()
    #    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


    ans = r.json().get('response')
    if not ans:
        print("DailyQueryLimit")
        if keyQueue.empty():
            print("queue is Empty")
            ans = "queue is Empty"
        else:
            values['key'] = keyQueue.get()
            r = requests.get(url, params=values)
            ans = r.json().get('response')

    slack_client.api_call("chat.postMessage", channel=channel, text=ans, \
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
    return None, None, None


# ~~~~~~~~~~~~~~~~~~MAIN INIT~~~~~~~~~~~~~~~~~~~~~
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
            time.sleep(READ_WEBSOCKET_DELAY / 2)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
