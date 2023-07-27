# voice_to_msg_bot

`voice_to_msg_bot` представляет собой `телеграм бота` который позволяет конвертировать голосовые сообщения в текст.
Бот позволяет конвертировать в текст не только сообщения отправленные ему напрямую, но также и пересланные сообщения.
Также реализовано логирование сообщений.

## Стек:

**Telebot**, **Soundfile**, **Speech_recognition**, **Dotenv**

## Как запустить проект:
Клонировать репозиторий:
```
git clone git@github.com:sntchweb/hw05_final.git
```
Cоздать и активировать виртуальное окружение:
```
py -m venv env
```
```
source venv/bin/activate
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
