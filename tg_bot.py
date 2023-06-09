import logging
import os
import uuid

import soundfile as sf
import speech_recognition as sr
import telebot
from dotenv import load_dotenv

from exceptions import SendMessageError

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    filename=f'{__file__}.log',
    mode='a',
    encoding='utf-8'
)
formatter = logging.Formatter('<%(asctime)s> [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

LANGUAGE = 'ru_RU'
BOT = telebot.TeleBot(os.getenv('BOT_TOKEN'))
VOICE_MSG_ERROR = 'Голосовое сообщние не распознано, попробуйте еще раз.'
SUCCESS_CONVERT_MSG = 'Голосовое сообщение конвертировано успешно'
FAIL_CONVERT_MSG = 'Ошибка при конвертации файла'
FAIL_DOWNLOAD_MSG = 'Ошибка при загрузке голосового сообщения'
SEND_MSG_ERROR = 'Ошибка при отправке сообщения в Telegram!'
SUCCESS_SENT_MSG = 'Бот успешно отправил сообщение в Telegram!'
SUCCESS_RECOGNIZE_MSG = 'Сообщение распознано успешно.'
SUCCESS_DOWNLOAD_MSG = 'Сообщение успешно скачано'


def google_recognize(wav_filename: str) -> str:
    recognize = sr.Recognizer()
    with sr.AudioFile(wav_filename) as source:
        audio_to_text = recognize.listen(source)
        try:
            message_text = recognize.recognize_google(
                audio_to_text,
                language=LANGUAGE
            )
            return message_text
        except Exception:
            logger.warning(VOICE_MSG_ERROR)
            return VOICE_MSG_ERROR
        else:
            logger.debug(SUCCESS_RECOGNIZE_MSG)


def download_file(message: dict, ogg_filename: str) -> None:
    """Функция скачивания голосового сообщения."""
    try:
        file_info = BOT.get_file(message.voice.file_id)
        download_file = BOT.download_file(file_info.file_path)
        with open(ogg_filename, 'wb') as new_file:
            new_file.write(download_file)
    except Exception as error:
        logger.critical(f'{FAIL_DOWNLOAD_MSG}: {error}')
    else:
        logger.debug(SUCCESS_DOWNLOAD_MSG)


def convert_file(ogg_filename: str, wav_filename: str) -> None:
    """Функция конвертирования гс из .ogg в .wav формат."""
    try:
        data, samplerate = sf.read(ogg_filename)
        sf.write(wav_filename, data, samplerate)
    except Exception as error:
        logger.error(f'{FAIL_CONVERT_MSG}: {error}')
    else:
        logger.debug(SUCCESS_CONVERT_MSG)


def send_message(message: dict, text: str) -> None:
    """Функция отправки сообщения в телеграм."""
    try:
        BOT.reply_to(message, text)
    except Exception:
        logger.error(SEND_MSG_ERROR)
        raise SendMessageError(SEND_MSG_ERROR)
    else:
        logger.debug(SUCCESS_SENT_MSG)


@BOT.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    ogg_filename, wav_filename = filename + '.ogg', filename + '.wav'
    try:
        download_file(message, ogg_filename)
        convert_file(ogg_filename, wav_filename)
        text = google_recognize(wav_filename)
        send_message(message, text)
        os.remove(ogg_filename)
        os.remove(wav_filename)
    except Exception as error:
        logger.critical(f'Сбой в работе программы: {error}')
    finally:
        logger.debug('-' * 50)


if __name__ == '__main__':
    BOT.polling()