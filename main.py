import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.strategy import FSMStrategy
from aiogram.utils.i18n import I18n
from redis.asyncio import Redis

from bot import handlers, middlewares
from config import settings
import loggers

logger = logging.getLogger(__name__)


async def main():
    """Point of entry"""

    logger.debug('Building bots')
    # I18n
    # Docs: https://docs.aiogram.dev/en/latest/utils/i18n.html
    i18n = I18n(path=settings.LOCALES_DIR, default_locale=settings.DEFAULT_LANGUAGE_CODE, domain=settings.I18N_DOMAIN)

    # Default bot properties.
    # Docs: https://docs.aiogram.dev/en/latest/api/defaults.html
    default_bot_properties = DefaultBotProperties(
        parse_mode=settings.PARSE_MODE,
    )

    # Create bots.
    bots = [Bot(token=_token, defaults=default_bot_properties) for _token in settings.TELEGRAM_BOT_TOKENS]

    # Bot redis-storage.
    # Docs: https://docs.aiogram.dev/en/latest/dispatcher/finite_state_machine/storages.html#redisstorage
    storage = RedisStorage(
        redis=Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True, )
    )

    # Create dispatcher.
    # Docs: https://docs.aiogram.dev/en/latest/dispatcher/dispatcher.html
    dispatcher = Dispatcher(
        storage=storage,
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
    )

    # Setup middlewares and handlers.
    middlewares.setup(dispatcher=dispatcher, i18n=i18n)
    handlers.setup(dispatcher=dispatcher)

    # Contextual data.
    extra_data = {
        'i18n': i18n,
    }

    await dispatcher.start_polling(*bots, **extra_data)


loggers.setup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning('Stopped!')
else:
    logger.warning('Use: python main.py')
