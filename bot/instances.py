import logging

from aiogram import Bot, Dispatcher, executor, types
from config import retrolan_bot_token
from types import SimpleNamespace
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

API_TOKEN = retrolan_bot_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler('app.log', 'w', 'utf-8')],
)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         one_time_keyboard=True  # чтобы сворачивалась
                         )

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='форма', url='https://forms.gle/dYLcPHocXMExP15X8')

# ikb.add(ib1, ib2)  # в одной строке
ikb.add(ib1)

text_storage = SimpleNamespace(
    help='<b>/start</b> - <em>начать работу с ботом</em>\n'
         '<b>/help</b> - <em>список команд</em>\n'
         '<b>/start_servey</b> - <em>начать опрос</em>\n'
    ,
    start='Привет я гаражный пук, хочешь попасть к нам и попердеть вместе с нами? '
          'Ответь на несколько вопросов, мне же надо познакомится поближе.',
    block='Вы уже прошли опрос.'
)

for button in text_storage.__dict__.keys():
    if button in ['start']:
        continue
    kb.add(KeyboardButton(f'/{button}'))


id_storage = dict(говорящий_гараж=-812977869, me=279478014)

surveys_holder = list()
surveys_complete_holder = set()


class Survey:
    def __init__(self, id):
        self.id = id
        self.switch = False
        self.counter = 0
        self.questions = [
            # 'Ссылка на акк в телеграме',
            'Звать то тебя как?',
            'Сколько годков тебе?',
            'Так мы тебя и запишем, а мог бы себя и попиздаче записать.'
            'Ты же понимаешь что от всех этих ответов зависит попадешь ты к нам или нет?',
            'Как там с деньгами вопрос обстоит?',
            'Хм... а ты вообще откуда? Есть соцсети?',
            'А чем вообще увлекаешься?',
            'И откуда ты услышал обо мне?',
            'Женат? или вилкой в глаз?',
            'А гамать во что любишь?',
        ]
        self.answers = []
        self.dump = None

    def next_question(self):
        try:
            question = self.questions[self.counter]
            self.counter += 1
            return question
        except IndexError:
            return False

    def update_answers(self, answer):
        self.answers.append(answer)

    def send(self):
        qna = []
        for i in range(len(self.questions)):
            text = ':\n'.join([f'<em>{self.questions[i]}</em>', self.answers[i]])
            qna.append(text)
        self.dump = '\n\n'.join(qna)
        return self.dump


