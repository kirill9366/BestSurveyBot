from aiogram import Bot

from aiogram.utils.i18n import I18n
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
import loggers


async def set_my_commands(bot: Bot, i18n: I18n):
    """
    Setting commands for bots with uses locales.
    :param bot:
    :param i18n:
    :return:
    """

    for locale in i18n.available_locales:
        await bot.set_my_commands(
            commands=[
                BotCommand(
                    command='start',
                    description=i18n.gettext('Start bot', locale=locale)
                )
            ],
            language_code=locale,
            scope=BotCommandScopeAllPrivateChats()
        )

    bot_me = await bot.get_me()
    loggers.bot.debug(f'Set commands for bot @{bot_me.username} id={bot_me.id} - \'{bot_me.full_name}\'')
