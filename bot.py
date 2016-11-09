from app.yisimsim import yisimsim
from app.debug import debug
import os
import exportSettings

if __name__ == "__main__":
    debug.get_instance().wlog("program started")

    bot=yisimsim(os.environ['SLACK_BOT_TOKEN'], os.environ['BOT_ID'], 1)
    debug.get_instance().wlog("bot instance created; bot ready to be run now")
    bot.run()

