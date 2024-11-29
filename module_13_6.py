from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb_reply = ReplyKeyboardMarkup(resize_keyboard = True)
bt_calc = KeyboardButton(text = 'Рассчитать')
bt_info = KeyboardButton(text = 'Информация')
kb_reply.row(bt_calc, bt_info)

kb_inline = InlineKeyboardMarkup()
bt_in_calc = InlineKeyboardButton(text = 'Рассчитать норму калорий',
                                  callback_data = 'calories')
bt_in_formula = InlineKeyboardButton(text = 'Формулы расчёта',
                                     callback_data = 'formulas')
kb_inline.row(bt_in_calc, bt_in_formula)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb_reply)

@dp.message_handler(text = 'Информация')
async def info(message):
    await message.answer('Привет! Я бот рассчитывающий количество калорий по формуле Миффлина-Сан Жеора.')

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = kb_inline)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6.25 х рост (см) - 5 * возраст (лет) + 5')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 4.92 * int(data['age']) + 5
    await message.answer(f'Количество калорий: {round(calories, 2)}')
    await state.finish()

@dp.message_handler()
async def all_messagr(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)