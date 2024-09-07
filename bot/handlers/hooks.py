from aiogram import Bot
from aiogram.utils.i18n import I18n

import loggers
from bot.utils.bot import set_my_commands


async def on_startup(bots: list[Bot], i18n: I18n):
    for bot in bots:
        await set_my_commands(bot=bot, i18n=i18n)

        bot_me = await bot.get_me()
        loggers.bot.info(f"Startup bot @{bot_me.username} id={bot_me.id} - '{bot_me.full_name}'")


async def on_shutdown(bots: list[Bot]):
    for bot in bots:
        await bot.delete_my_commands()

        bot_me = await bot.get_me()
        loggers.bot.info(f"Shutdown bot @{bot_me.username} id={bot_me.id} - '{bot_me.full_name}'")
