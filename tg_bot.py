import logging
import telebot

BOT_TOKEN = '6130737728:AAEH_8HaguB05phCGzOI-GZQxkBfnCFx8-E'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌️ ")


bot.infinity_polling()
