import asyncio
import logging
import os
import uuid

import soundfile as sf
import speech_recognition as sr
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions
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
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] => %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

ERROR_MSG = 'Сбой в работе программы'
VOICE_MSG_ERROR = 'Голосовое сообщние не распознано, попробуйте еще раз.'
SUCCESS_CONVERT_MSG = 'Успешная конвертация сообщения.'
FAIL_CONVERT_MSG = 'Ошибка при конвертации файла!'
FAIL_DOWNLOAD_MSG = 'Ошибка при загрузке голосового сообщения!'
SEND_MSG_ERROR = 'Ошибка при отправке сообщения в Telegram!'
SUCCESS_SENT_MSG = 'Успешная отправка сообщения в Telegram.'
SUCCESS_RECOGNIZE_MSG = 'Голосовое сообщение распознано успешно.'
SUCCESS_DOWNLOAD_MSG = 'Голосовое сообщение успешно скачано.'
LANGUAGE = 'ru-RU'

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)
logger = logging.getLogger(__name__)


async def download_voice_file(
        message: types.Message,
        ogg_filename: str
) -> None:
    """
    Асинхронная функция скачивания голосового сообщения.
    -принимает сообщение формата types.Message и сконвертированное
    название файла(тип str) для скачиавания.
    """
    try:
        file_info = await bot.get_file(message.voice.file_id)
        download_file = await bot.download_file(file_info.file_path)
        with open(ogg_filename, 'wb') as new_file:
            new_file.write(download_file.read())
    except exceptions.TelegramAPIError as error:
        logger.critical(f'{FAIL_DOWNLOAD_MSG}: {error}')
    else:
        logger.info(SUCCESS_DOWNLOAD_MSG)


async def recognize_voice_message(wav_filename: str) -> str:
    """
    Асинхронная функция конвертации .wav файла в текст.
    -принимает название(тип str) файла для конвертации.
    -возвращает текст(тип str).
    """
    recognize = sr.Recognizer()
    with sr.AudioFile(wav_filename) as source:
        audio_to_text = recognize.listen(source)
        try:
            message_text = recognize.recognize_google(
                audio_to_text,
                language=LANGUAGE
            )
        except Exception:
            logger.warning(VOICE_MSG_ERROR)
            return VOICE_MSG_ERROR
        else:
            logger.info(SUCCESS_RECOGNIZE_MSG)
            return message_text


async def convert_voice_file(ogg_filename: str, wav_filename: str) -> None:
    """
    Асинхронная функция конвертирования голосового сообщения
    из .ogg в .wav формат.
    -принимает название файла(тип str) который нужно конвертировать и
    название файла(тип str) для результата конвертации.
    """
    try:
        data, samplerate = sf.read(ogg_filename)
        sf.write(wav_filename, data, samplerate)
    except Exception as error:
        logger.error(f'{FAIL_CONVERT_MSG}: {error}')
    else:
        logger.info(SUCCESS_CONVERT_MSG)


async def send_message(message: types.Message, text: str) -> None:
    """
    Асинхронная функция отправки сообщения в телеграм.
    -принимает сообщение и распознанный текст, который
    необходимо отправить пользователю.
    """
    try:
        await message.answer(text)
    except Exception:
        logger.error(SEND_MSG_ERROR)
        raise SendMessageError(SEND_MSG_ERROR)
    else:
        logger.info(f'{SUCCESS_SENT_MSG} user-id:{message.from_user.id}')


@dp.message_handler(content_types=['voice'])
async def voice_processing(message: types.Message):
    """Основная логика."""

    filename = str(uuid.uuid4())
    ogg_filename, wav_filename = filename + '.ogg', filename + '.wav'
    try:
        await download_voice_file(message, ogg_filename)
        await convert_voice_file(ogg_filename, wav_filename)
        text = await recognize_voice_message(wav_filename)
        await send_message(message, text)
        os.remove(ogg_filename)
        os.remove(wav_filename)
    except Exception as error:
        logger.critical(f'{ERROR_MSG}: {error}')
    finally:
        logger.debug('-' * 50)


async def main():
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
