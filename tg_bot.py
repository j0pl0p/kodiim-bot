import logging
import os
import telebot
import requests
import re

BOT_TOKEN = '6130737728:AAEH_8HaguB05phCGzOI-GZQxkBfnCFx8-E'
URL_REGEX = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN)

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Новая камера')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Привет, я могу уведомить тебя если кто-то придет в гости и скинуть фото",
        reply_markup=keyboard1
    )


@bot.message_handler(func=lambda x: x.text.lower() == 'новая камера')
def get_link(message):
    new_msg = bot.reply_to(
        message,
        'Введите URL:',
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(new_msg, get_video)


def get_video(message):
    link = message.text
    if re.fullmatch(URL_REGEX, link):
        new_msg = bot.reply_to(message, 'Теперь отправьте видео')
        bot.register_next_step_handler(new_msg, download_video, link)
    else:
        new_msg = bot.reply_to(message, 'Некорректный URL, попробуйте еще раз')
        bot.register_next_step_handler(new_msg, get_video)


def download_video(message, url):
    # with open('log.txt', 'w') as log:
    #    print(message, log)
    # print(message)
    if not os.path.exists(f'user_data/{message.from_user.id}'):
        os.makedirs(f'user_data/{message.from_user.id}')
    vid_id = message.video.file_id
    # print('id received')
    vid_url = f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={vid_id}'
    vid_file = requests.get(vid_url).json()["result"]["file_path"]
    vid_download_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{vid_file}'
    vid_data = requests.get(vid_download_url)
    with open(f'user_data/{message.from_user.id}/video.mp4', 'wb') as f:
        f.write(vid_data.content)
    bot.reply_to(
        message,
        f'Видео сохранено и будет обработано в ближайшее время. \nURL: {url}, \nПуть к видео: user_data/{message.from_user.id}/video.mp4'
    )


bot.infinity_polling()
