from aiogram import executor
from bot.instances import dp
from bot.handlers import on_startup


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)