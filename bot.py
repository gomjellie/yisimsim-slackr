from app.yisimsim import yisimsim
import os
import exportSettings

if __name__ == "__main__":
    bot=yisimsim(os.environ['SLACK_BOT_TOKEN'], os.environ['BOT_ID'], 1)
    bot.run()

