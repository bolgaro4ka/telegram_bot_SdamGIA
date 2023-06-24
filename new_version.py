from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from datetime import datetime
from sdamgia import SdamGIA
from random import sample
import random

from transport_layer import *
from consts import *
from utils import *

#normal_q = [24639, 24337, 5511, 12577, 12625, 10651, 6379, 22491, 13285, 3755, 1001, 2797, 16315, 11569, 10663, 2443,
#            23939, 24145, 14225, 14451, 48907, 2515, 24317, 4903, 27044, 17537, 12009, 12133, 5035, 14929, 18389, 18611,
#            4711, 22955, 11843, 10983]
bot = Bot(token="YOUR_TELEGRAM_API_KEY")
dp = Dispatcher(bot, storage=MemoryStorage())
users_data = {}
sdamgia = SdamGIA()
TESTING = False


@dp.message_handler(commands=["GM"])
async def start(msg: types.Message):
    global TESTING
    TESTING = True
    await bot.send_message(msg.from_user.id, "Режим разработчика включен!")


@dp.message_handler(commands=["NO_GM"])
async def start(msg: types.Message):
    global TESTING
    TESTING = False
    await bot.send_message(msg.from_user.id, "Режим разработчика выключен!")


@dp.message_handler(commands=["start"])
async def cmd_start(msg: types.Message):
    await bot.send_message(msg.from_user.id, START_MESSAGE)


@dp.message_handler(commands=["help"])
async def help_(msg: types.Message):
    await bot.send_message(msg.from_user.id, get_help_message(), )


@dp.message_handler(commands=["info"])
async def info(msg: types.Message):
    ans = get_cheat_image()
    if ans is None:
        await bot.send_message(msg.from_user.id, "Ошибка загрузки")
    else:
        await bot.send_message(msg.from_user.id, "Вся теория в одном файле:")
        await bot.send_photo(msg.from_user.id, ans)


@dp.message_handler(commands=["calc"])
async def calc(msg: types.Message):
    arg = msg.get_args()
    await bot.send_message(msg.from_user.id, eval(arg))


@dp.message_handler(commands=["trainer"])
async def trainer(msg: types.Message):
    global id
    id = random.randint(1000, 50000)
    #id = random.choice(normal_q)
    subject = 'math'
    if type(sdamgia.get_problem_by_id(subject, str(id))['condition']['text']) is None:
        id+=1
    if "Найдите значение выражения" in str(
            sdamgia.get_problem_by_id(subject, str(id))['condition']['text']) or "Найдите корень уравнения" in str(
        sdamgia.get_problem_by_id(subject, str(id))['condition']['text']) or (
            "треугольник" in str(sdamgia.get_problem_by_id(subject, str(id))['condition']['text'])) or (
            "периметр" in str(sdamgia.get_problem_by_id(subject, str(id))['condition']['text'])) or (
            "площад" in str(sdamgia.get_problem_by_id(subject, str(id))['condition']['text'])) or (
            "рисун" in str(sdamgia.get_problem_by_id(subject, str(id))['condition']['text'])) or (
            "таблиц" in str(sdamgia.get_problem_by_id(subject, str(id))['condition']['text'])):
        await bot.send_message(msg.from_user.id, str(str("Картинка задачи/примера: ") + str(
            sdamgia.get_problem_by_id(subject, str(id))['condition']['images'][0])))
    ans = sdamgia.get_problem_by_id(subject, id)
    await bot.send_message(msg.from_user.id, ans['condition']['text'])
    await bot.send_message(msg.from_user.id, str(str("Номер задачи на РешуГИА: ") + str(
        ans['id']) + " (если задача отобразилась некорректно, то перейди по ссылке: ") + str(ans['url']) + ")")
    kb = [
        [types.KeyboardButton(text="показать решение")],
        [types.KeyboardButton(text="exit")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Введите ответ:"
    )
    await msg.answer("Введите ответ:", reply_markup=keyboard)
    # await bot.send_message(msg.from_user.id, ans['answer'])
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(GameStates.WAIT_MOVE[0])


@dp.message_handler()
async def error_type(msg: types.Message):
    text = msg.from_user.full_name + ', "' + msg.text + '" не является командой этого бота'
    await bot.send_message(msg.from_user.id, text)


@dp.message_handler(state=GameStates.WAIT_MOVE[0])
async def trainer_work(msg: types.Message):
    uid = msg.from_user.id
    subject = 'math'
    tmp = sdamgia.get_problem_by_id(subject, id)
    if msg.text == "exit":
        await msg.reply("Тренажёр выключен", reply_markup=types.ReplyKeyboardRemove())
        # await bot.send_message(uid, "Тренажёр выключен")
        state = dp.current_state(user=uid)
        await state.reset_state()
        return
    ans = msg.text
    if str(ans) == 'показать решение':
        await bot.send_message(uid, tmp['solution']['text'])
        await msg.reply("В следующий раз похожую задачу получится решить самому! Нажимай на /trainer,"
                        " чтобы решить следующее задание", reply_markup=types.ReplyKeyboardRemove())
        state = dp.current_state(user=uid)
        await state.reset_state()
    elif str(ans) in tmp['solution']['text'][-10:]:
        await msg.reply("Правильный ответ! Нажимай на /trainer,"
                        " чтобы решить следующее задание", reply_markup=types.ReplyKeyboardRemove())
        state = dp.current_state(user=uid)
        await state.reset_state()
    else:
        await bot.send_message(uid, 'Попробуй еще раз')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
