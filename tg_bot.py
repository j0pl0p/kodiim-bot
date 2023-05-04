import logging
from telegram.ext import Application, MessageHandler, filters

BOT_TOKEN = '6130737728:AAEH_8HaguB05phCGzOI-GZQxkBfnCFx8-E'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    if update.message.text.lower().startswith('меня зовут'):
        await update.message.reply_text('Hello, ' + ' '.join(update.message.text.split()[2:]))


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
