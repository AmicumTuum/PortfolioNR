from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.helper import HelperMode
import openai


tg_token = ''
oai_token = ''


openai.api_key = oai_token
bot = Bot(token=tg_token, timeout=None)
dp = Dispatcher(bot, storage=MemoryStorage())


def generate_response(prompt):
    completion = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )
    message = completion.choices[0].text
    return message

def generate_responseQA(prompt1):
    completion = openai.Completion.create(
    model="text-davinci-003",
    prompt1="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\n",
    temperature=0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\n"]
    )  
    message = completion.choices[0].text
    return message

class Talk(StatesGroup):
    mode = HelperMode.snake_case
    ACTIVE = State()


@dp.message_handler(commands=['help', 'start'])
async def process_help_command(message: types.Message):
    await message.reply(
        '— Что бы включить бота напиши "Куку"\n'
        '— Что бы выключить - "Пока"\n'
        '— Бот отвечает только тому кто его разбудил\n'
        '— Попросить уснуть бота могут все'
    )


@dp.message_handler()
async def process_help_command(message: types.Message, state: FSMContext):
    if message.text.lower().startswith('куку'):
        await Talk.ACTIVE.set()
        await state.update_data(user_id=message['from']['id'])
        await message.reply('Привет, я проснулся. Напиши "Пока", если нужно что бы я уснул')


@dp.message_handler(state=Talk.ACTIVE)
async def process_help_command(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text.lower().startswith('пока'):
        await message.reply('Пока!')
        await state.finish()
    elif user_data['user_id'] == message['from']['id']:
        await message.reply(generate_response(message.text))


if __name__ == '__main__':
    executor.start_polling(dp)
