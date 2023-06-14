# voice_to_msg_bot

voice_to_msg_bot представляет собой `телеграм бота` который позволяет конвертировать голосовые сообщения в текст.
Бот позволяет конвертировать в текст не только сообщения отправленные ему напрямую, но также и пересланные сообщения.

## Используемые библиотеки:

- **Telebot**

- **Soundfile**
```
Конвертирует формат .ogg в .wav для дальнейшего распознавания.
```

- **Speech_recognition**
```
Конвертирует звуковой файл формата .wav в текст.
```

- **Dotenv**
```
Подгружает переменные окружения из .env файла.
```