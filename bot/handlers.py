from bot.helpers import survey_flow, check_blacklist
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from bot.instances import bot, dp, surveys_holder, surveys_complete_holder, text_storage, Survey


async def on_startup(_):
    print("I'm alive")


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=text_storage.help,
                           parse_mode='HTML',
                           reply_markup=ReplyKeyboardRemove()
                           )
    await message.delete()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=text_storage.start)
    await message.delete()
    await message.answer(text='/start_survey чтобы начать опрос')


@dp.message_handler(commands=['start_survey'])
async def links_command(message: types.Message):
    # if message.from_user.id not in surveys_complete_holder:
    if not check_blacklist(message.from_user.id):
        survey = Survey(id=message.from_user.id)
        survey.switch = True
        surveys_holder.append(survey)
        await message.delete()
        await message.answer(survey.next_question())
    else:
        await message.delete()
        await bot.send_message(chat_id=message.from_user.id,
                               text=text_storage.block,
                               )


@dp.message_handler(content_types=['text'])
async def send_sticker_id(message: types.Message):
    await survey_flow(message)

