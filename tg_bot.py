import logging
import os
import telebot
import requests
import re
import cv2

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
    if not os.path.exists(f'user_data/{message.from_user.id}/frames'):
        os.makedirs(f'user_data/{message.from_user.id}/frames')
    # print('id received')
    vid_file = \
    requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={message.video.file_id}').json()["result"][
        "file_path"]
    vid_data = requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{vid_file}')
    with open(f'user_data/{message.from_user.id}/video.mp4', 'wb') as f:
        f.write(vid_data.content)

    bot.reply_to(
        message,
        f'Подождите, видео обрабатывается...'
    )

    cap = cv2.VideoCapture(f'user_data/{message.from_user.id}/video.mp4')
    frames_amount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(min(frames_amount, 60)): # 60 кадров будет достаточно
        success, frame = cap.read()
        if not success:
            break
        cv2.imwrite(f'user_data/{message.from_user.id}/frames/{i + 1}.png', frame)

    bot.reply_to(
        message,
        f'Видео сохранено и будет обработано ИИ в ближайшее время.'
    )


bot.infinity_polling()
