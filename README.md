# voice_to_msg_bot - телеграм бот, конвертирующий голосовые сообщения в текст.

`voice_to_msg_bot` представляет собой `телеграм бота` который позволяет конвертировать голосовые сообщения в текст.
Бот позволяет конвертировать в текст не только сообщения отправленные ему напрямую, но также и пересланные сообщения.
Также реализовано логирование.

## Как запустить проект:
Клонировать репозиторий:
```
git clone git@github.com:sntchweb/voice_to_msg_bot.git
```
Cоздать и активировать виртуальное окружение:
```
py -m venv env
```
```
source venv/bin/activate
```
Создать файл `.env` и поместить в него ваш BOT_TOKEN, например:
```
BOT_TOKEN = '6240622552:AZGOLU287dCTBwDdntv3yzQIoyqUODD-YZap'
```
Установить зависимости из файла requirements.txt:
```
py -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Запустить бота:
```
py tg_bot.py
```
Если ошибка soundfile:
```
py -m pip install --force-reinstall soundfile
```

## Стек технологий:

- Python
- Telebot
- Soundfile
- Speech_recognition
- Dotenv
## Автор:
Лашин Артём
