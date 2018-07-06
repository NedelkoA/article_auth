import telepot
from telepot.loop import MessageLoop
from .. import models

TOKEN = '606061796:AAFsveXNHQ75CssfRwJbxH1LrSo8HG5SX84'
bot = telepot.Bot(TOKEN)


def handle(msg):
    if 'entities' in msg and msg['entities'][0]['type'] == 'phone_number':
        try:
            profile = models.UserProfile.objects.get(telephone=msg['text'])
            profile.telegram_id = msg['chat']['id']
            profile.save()
        except models.UserProfile.DoesNotExist:
            bot.sendMessage(msg['chat']['id'], 'Please enter valid phone number')
    elif msg['text'] == '/start':
        bot.sendMessage(msg['chat']['id'], 'Please enter your phone number. Format: +380xxxxxxxxx')


MessageLoop(bot, handle).run_as_thread()
