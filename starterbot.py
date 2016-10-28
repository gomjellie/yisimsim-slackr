import os
import time
import sqlite3
from slackclient import SlackClient

# startbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instant Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
con = sqlite3.connect("chat.db")
print("chat.db created !")
cursor = con.cursor()
print("cursor created !")
#cursor.execute("CREATE TABLE chatlog(Quest text, Ans text)")
isLearning = False
prevQuest = ''

def handle_command(command, channel):
    global con
    global isLearning
    global cursor
    global prevQuest
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    if not isLearning:
        print("if not isLearning")
        cursor = con.execute("SELECT * FROM chatlog WHERE Quest=?", (command,))
        response = cursor.fetchone()
        if not response:
            print("if not response")

            #cursor.execute("INSERT INTO chatlog VALUES('{}', 'what can i say to that?')".format(command))
            #cursor.execute("INSERT INTO chatlog VALUES('" + command + "', 'what can i say to that?')")
            prevQuest = command
            response = 'what can i say to that?'
            isLearning = True
        else:
            print("if response")
            response = response[1]
            isLearning = False;

        #if command.startswith(EXAMPLE_COMMAND):
            #response = "뭐하라고?"
        
    else: #if isLearning == True
    	print("if isLearning")
    	t = (prevQuest, command)
    	cursor.execute("INSERT INTO chatlog VALUES (?,?)", t)
    	response = "i've learned well"
    	isLearning = False;
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    



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
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                        output['channel']
    return None, None



#~~~~~~~~~~~~~~~~~~MAIN INIT~~~~~~~~~~~~~~~~~~~~~
if __name__=="__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
