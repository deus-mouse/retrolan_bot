
from bot.instances import bot, surveys_holder, id_storage, logging, blacklist_file
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import openpyxl


async def survey_flow(message):
    '''
    message.from_user.url = tg://user?id=457526700
    message.chat.id = 457526700
    :param message:
    :return:
    '''
    for index in range(len(surveys_holder)):
        survey = surveys_holder[index]
        if survey.id == message.from_user.id and survey.switch:
            survey.update_answers(message.text)
            question = survey.next_question()
            if question:
                await message.answer(question)
            else:
                # survey.switch = False
                button_url = message.from_user.url
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(text=message.from_user.username, url=button_url))
                await bot.send_message(id_storage['me'], text=survey.send(), parse_mode='HTML',
                                       reply_markup=markup)
                await message.answer('Я подумаю, посовещаюсь с гаражниками, и дам свой ответ 🤖')
                # surveys_complete_holder.add(message.from_user.id)
                blacklist_update(message.from_user.id)
                surveys_holder.pop(index)


def check_blacklist(id) -> bool:
    book = openpyxl.open(blacklist_file)
    sheet = book.active
    # print(f'{sheet["A2"].value=}')
    # print(f'{sheet[2][0].value=}')
    column = sheet['A']
    blacklist = [item.value for item in column]
    return id in blacklist


def blacklist_update(id):
    print(f'{id=}')
    book = openpyxl.open(blacklist_file)
    sheet = book.active
    column = sheet['A']
    sheet[len(column)+1][0].value = id
    book.save(blacklist_file)
    book.close()
