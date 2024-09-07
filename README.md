# Aiogram telegram bot template

## О шаблоне

Шаблон для написания телеграмм ботов с помощью aiogram 3.8.0

* Реализован Антифлуд
* Используется мультиязычность (в т.ч реализованы фильтры)
* Кеширование
* Используется Redis
* *Запуск нескольких ботов

***В шаблоне используется Long Polling, а не Webhook**

## Зависимости

* [python 3.10.x](%3Chttps://www.python.org/downloads/release/python-3108/%3E)
* [aiogram 3.8.0](https://docs.aiogram.dev/en/latest/dispatcher/finite_state_machine/storages.html)
* [babel 2.x.x](https://pypi.org/project/Babel/)
* [redis 5.x.x](https://pypi.org/project/redis/)
* [environs 11.x.x](https://pypi.org/project/environs/)
* [cachetools 5.x.x](https://pypi.org/project/cachetools/)
* [pytimeparse 1.x.x](https://pypi.org/project/pytimeparse/)

## Антифлуд

В шаблоне реализован антифлуд.

Для его настройки необходимо:

* Определить константу THROTTLES в файле config/settings.py.
  > Пример
  > ```
  > THROTTLES = {"default": "5/1s", "some": "1/1min"}
  >```
  > default - 5 сообщений в секунду
  > some - 1 сообщениe в минуту

* Добавить декоратор bot.utils.throttling.rate_limit к обработчику сообщения.
  > Пример
  >```
  > from bot.utils.throttling import rate_limit
  >
  > ...
  >
  > @rate_limit(name="default")
  > @router.message()
  > async def my_handler(message):
  >     pass
  > ```
  >
  > При привышении лимита update не дойдет до вашего обработчика.

 
* Обработать событие можно в методе `bot.middlewares.MessageThrottlingMiddleware._process_message_throttling()`
  >
  > Пример оповещения пользователя, что он привысил лимит.
  > ```  
  > class MessageThrottlingMiddleware(BaseMiddleware):
  >     
  >     ...
  >     
  >     async def _process_message_throttling(self, name: str, bot: Bot, message: Message):
  >         key = self._make_key(bot, message)
  >         number_of_messages = parse_number_of_messages_by_throttle_name(name)
  >         if message.chat.type == 'private':
  >             if self.storage[name][key] == number_of_messages + 1:
  >                 await message.answer("Не так быстро! Немного подождите!")
  > ```
  > Пример блокировки пользователя в чате при привышении лимита.  
  > ```  
  > 
  > class MessageThrottlingMiddleware(BaseMiddleware):
  >     
  >     ...
  >    
  >     async def _process_message_throttling(self, name: str, bot: Bot, message: Message):
  >         key = self._make_key(bot, message)
  >         number_of_messages = parse_number_of_messages_by_throttle_name(name)
  >         if message.chat.type in {'group', 'supergroup'}:
  >             if self.storage[name][key] == number_of_messages + 1:
  >                     await message.chat.ban_sender_chat(message.from_user.id)
  > ```
  

## Переменные окружения
Переменные окружения задаются в файле .env в корне проекта

* TELEGRAM_BOT_TOKENS=123456789:botapitoken
* REDIS_HOST=localhost
* REDIS_PORT=6379

## Файл с настройками

Все настройки относящиеся к проекту вы можете хранить в файле config/settings.py

* `BASE_DIR` - Абсолютный путь до проекта
* `ENV_FILE` - Абсолютный путь до файла переменных окружения
* `LOGGING_CONF_FILE` - Абсолютный путь до файла конфигурации логгирования
* `LOCALES_DIR` - Абсолютный путь до каталога с локалями
* `I18N_DOMAIN`- Домен i18n
* `DEFAULT_LANGUAGE_CODE` - Локаль по умолчанию, если не удалось ее определить
* `TELEGRAM_BOT_TOKENS` - API Токен/токены через ,
* `PARSE_MODE` - Парсер сообщения телеграм
* `THROTTLING_KEY` - Ключ для антифлуда (не рекомендуется менять)
* `THROTTLES` - Настройки лимитов антифлуда
* `REDIS_HOST` - Хост Redis
* `REDIS_PORT` - Порт Redis


## Запуск бота

* Создайте файл `.env` в корне проекта и заполните его по примеру из файла 

* > Запустите в терминале
  > ```
  > poetry install
  > ```
  >
  > ```
  > poetry shell
  > ```
  >
  > ```
  > python main.py
  > ```

    


## Разворачивание при помощи Docker

* Создайте файл `.env` в корне проекта и заполните его по примеру из файла `.env.example`.

* > Запустите в терминале
  > ```
  > docker build -t telegram-bot .
  > ```
  >
  > ```
  > docker run telegram-bot
  > ```

## FAQ

* `Как установить poetry? <https://python-poetry.org/docs/>`_
* `Как установить docker? <https://docs.docker.com/desktop/install/windows-install/>`_
