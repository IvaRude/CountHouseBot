from aiogram import types
from aiogram.utils.helper import Helper, HelperMode, ListItem

from cian.async_cian_average import async_find_average
from cian.cian_average import find_average
from dispatcher import bot, dp
from keyboards import keyboard1, keyboard2, \
    object_type_keyboard, room_keyboard, final_keyboard


class TestStates(Helper):
    mode = HelperMode.snake_case

    STATE_0 = ListItem()
    STATE_1 = ListItem()
    STATE_2 = ListItem()
    STATE_3 = ListItem()
    STATE_4 = ListItem()
    STATE_5 = ListItem()
    STATE_6 = ListItem()
    STATE_7 = ListItem()
    FINAL_STATE = ListItem()


LINK = ""
link_params = {}


@dp.message_handler(commands=["start", "help"])
async def info(message: types.Message):
    await message.answer("Привет! Я могу посчитать среднюю цену квартиры и среднюю цену за квадратный метр в Москве.\n"
                         "Чтобы начать введи /count или можешь сразу скинуть ссылку своего поиска на сайте "
                         "https://www.cian.ru/")


async def count_cian(user_id, link):
    await bot.send_message(user_id, "Сейчас посчитаю...")
    res = await async_find_average(link)
    await bot.send_message(user_id, res)


async def make_final_question():
    question = ""
    for key in link_params:
        value = link_params[key]
        if key == "object_type":
            if value == "1":
                question += "Вторичка\n"
            elif value == "2":
                question += "Новостройка\n"
            else:
                question += "Вторичка или новостройка\n"
        elif key == "room2" and value == "1":
            question += "Двушка\n"
        elif key == "room3" and value == "1":
            question += "Трешка\n"
        elif key == "minprice":
            question += f"Цена от {value}"
        elif key == "maxprice":
            question += f" до {value}\n"
        elif key == "foot_min":
            question += f"Минут до метро {value}\n"
        elif key == "mintarea":
            question += f"Общая площадь от {value}\n"
        elif key == "minkarea":
            question += f"Площадь кухни от {value}"
        elif key == "maxkarea":
            question += f" до {value}"
    return question


async def ask_final_question(user_id):
    question = await make_final_question()
    await bot.send_message(user_id, question)
    await bot.send_message(user_id, "Все верно?", reply_markup=final_keyboard)


async def make_link():
    LINK = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&region=1&offer_type=flat&is_first_floor=0&ipoteka=1&only_flat=1&only_foot=2"
    METRO = "&metro%5B0%5D=2&metro%5B100%5D=140&metro%5B101%5D=141&metro%5B102%5D=142&metro%5B103%5D=143&metro%5B104%5D=145&metro%5B105%5D=146&metro%5B106%5D=147&metro%5B107%5D=148&metro%5B108%5D=149&metro%5B109%5D=150&metro%5B10%5D=13&metro%5B110%5D=151&metro%5B111%5D=154&metro%5B112%5D=155&metro%5B113%5D=156&metro%5B114%5D=159&metro%5B115%5D=229&metro%5B116%5D=236&metro%5B117%5D=237&metro%5B118%5D=272&metro%5B119%5D=275&metro%5B11%5D=14&metro%5B120%5D=281&metro%5B121%5D=283&metro%5B122%5D=286&metro%5B123%5D=287&metro%5B124%5D=289&metro%5B125%5D=290&metro%5B126%5D=291&metro%5B127%5D=296&metro%5B128%5D=309&metro%5B129%5D=311&metro%5B12%5D=15&metro%5B130%5D=337&metro%5B131%5D=338&metro%5B132%5D=339&metro%5B133%5D=350&metro%5B134%5D=351&metro%5B135%5D=352&metro%5B136%5D=361&metro%5B137%5D=362&metro%5B138%5D=363&metro%5B13%5D=16&metro%5B14%5D=18&metro%5B15%5D=20&metro%5B16%5D=21&metro%5B17%5D=27&metro%5B18%5D=29&metro%5B19%5D=30&metro%5B1%5D=3&metro%5B20%5D=33&metro%5B21%5D=35&metro%5B22%5D=36&metro%5B23%5D=37&metro%5B24%5D=38&metro%5B25%5D=40&metro%5B26%5D=42&metro%5B27%5D=43&metro%5B28%5D=44&metro%5B29%5D=44&metro%5B2%5D=4&metro%5B30%5D=45&metro%5B31%5D=46&metro%5B32%5D=46&metro%5B33%5D=47&metro%5B34%5D=49&metro%5B35%5D=50&metro%5B36%5D=53&metro%5B37%5D=54&metro%5B38%5D=55&metro%5B39%5D=56&metro%5B3%5D=4&metro%5B40%5D=57&metro%5B41%5D=58&metro%5B42%5D=60&metro%5B43%5D=61&metro%5B44%5D=62&metro%5B45%5D=63&metro%5B46%5D=64&metro%5B47%5D=66&metro%5B48%5D=68&metro%5B49%5D=70&metro%5B4%5D=5&metro%5B50%5D=71&metro%5B51%5D=71&metro%5B52%5D=72&metro%5B53%5D=73&metro%5B54%5D=74&metro%5B55%5D=75&metro%5B56%5D=77&metro%5B57%5D=78&metro%5B58%5D=79&metro%5B59%5D=80&metro%5B5%5D=8&metro%5B60%5D=81&metro%5B61%5D=84&metro%5B62%5D=85&metro%5B63%5D=86&metro%5B64%5D=87&metro%5B65%5D=91&metro%5B66%5D=93&metro%5B67%5D=96&metro%5B68%5D=97&metro%5B69%5D=98&metro%5B6%5D=8&metro%5B70%5D=100&metro%5B71%5D=102&metro%5B72%5D=103&metro%5B73%5D=104&metro%5B74%5D=105&metro%5B75%5D=107&metro%5B76%5D=108&metro%5B77%5D=110&metro%5B78%5D=112&metro%5B79%5D=113&metro%5B7%5D=9&metro%5B80%5D=114&metro%5B81%5D=115&metro%5B82%5D=115&metro%5B83%5D=116&metro%5B84%5D=117&metro%5B85%5D=118&metro%5B86%5D=119&metro%5B87%5D=120&metro%5B88%5D=121&metro%5B89%5D=122&metro%5B8%5D=11&metro%5B90%5D=123&metro%5B91%5D=124&metro%5B92%5D=125&metro%5B93%5D=128&metro%5B94%5D=129&metro%5B95%5D=130&metro%5B96%5D=131&metro%5B97%5D=132&metro%5B98%5D=133&metro%5B99%5D=134&metro%5B9%5D=12"
    LINK += METRO
    for key in link_params:
        value = link_params[key]
        if value:
            LINK += f"&{key}={value}"
    return LINK


async def next_question(user_id):
    state = dp.current_state(user=user_id)
    state = await state.get_state()
    if state == TestStates.STATE_0[0]:
        await bot.send_message(user_id, "Выбери", reply_markup=object_type_keyboard)
    elif state == TestStates.STATE_1[0]:
        await bot.send_message(user_id, "Сколько комнат?", reply_markup=room_keyboard)
    elif state == TestStates.STATE_2[0]:
        await bot.send_message(user_id, "Цена от скольки?")
    elif state == TestStates.STATE_3[0]:
        await bot.send_message(user_id, "Цена до скольки?")
    elif state == TestStates.STATE_4[0]:
        await bot.send_message(user_id, "Максимальное число минут до метро пешком?")
    elif state == TestStates.STATE_5[0]:
        await bot.send_message(user_id, "Общая площадь от?")
    elif state == TestStates.STATE_6[0]:
        await bot.send_message(user_id, "Кухня от?")
    elif state == TestStates.STATE_7[0]:
        await bot.send_message(user_id, "Кухня до?")
    elif state == TestStates.FINAL_STATE[0]:
        await ask_final_question(user_id)


@dp.message_handler(text="/count")
async def get_message(message: types.Message):
    await message.answer("Дашь ссылку?", reply_markup=keyboard1)


@dp.callback_query_handler(lambda c: c.data == "btn1")
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Жду ссылку)')


@dp.callback_query_handler(lambda c: c.data == "btn2")
async def process_callback_button2(callback_query: types.CallbackQuery):
    # await bot.send_message(callback_query.from_user.id, 'Стандартный вариант?', reply_markup=keyboard2)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(TestStates.all()[1])
    await bot.send_message(callback_query.from_user.id, "Выбери", reply_markup=object_type_keyboard)


# @dp.callback_query_handler(lambda c: c.data == "btn5")
# async def process_callback_button5(callback_query: types.CallbackQuery):
#     state = dp.current_state(user=callback_query.from_user.id)
#     await state.set_state(TestStates.all()[1])
#     await bot.send_message(callback_query.from_user.id, "Выбери", reply_markup=object_type_keyboard)


async def feel_object_type(obj_type):
    global link_params
    link_params["object_type"] = obj_type


@dp.callback_query_handler(lambda c: c.data in ["btn6", "btn7", "btn8"],
                           state=TestStates.STATE_0 | TestStates.FINAL_STATE)
async def object_type_question(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    cur_state = await state.get_state()
    if cur_state in TestStates.STATE_0:
        await state.set_state(TestStates.STATE_1[0])
    if callback_query.data == "btn6":
        await feel_object_type("1")
    elif callback_query.data == "btn7":
        await feel_object_type("2")
    else:
        await feel_object_type(None)
    await next_question(callback_query.from_user.id)


async def feel_room(num_of_rooms):
    global link_params
    if num_of_rooms == "2":
        link_params["room2"] = "1"
        link_params["room3"] = None
    elif num_of_rooms == "3":
        link_params["room2"] = None
        link_params["room3"] = "1"
    elif num_of_rooms == "both":
        link_params["room2"] = "1"
        link_params["room3"] = "1"


@dp.callback_query_handler(lambda c: c.data in ["btn9", "btn10", "btn9_10"],
                           state=TestStates.STATE_1 | TestStates.FINAL_STATE)
async def object_type_question(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    cur_state = await state.get_state()
    if cur_state in TestStates.STATE_1:
        await state.set_state(TestStates.STATE_2[0])
    if callback_query.data == "btn9":
        await feel_room("2")
    elif callback_query.data == "btn10":
        await feel_room("3")
    else:
        await feel_room("both")
    await next_question(callback_query.from_user.id)


# Цена от
@dp.message_handler(state=TestStates.STATE_2 | TestStates.FINAL_STATE)
async def object_type_question(message: types.Message):
    global link_params
    state = dp.current_state(user=message.from_user.id)
    cur_state = await state.get_state()
    if message.text.isdigit():
        link_params["minprice"] = message.text
        if cur_state in TestStates.STATE_2:
            await state.set_state(TestStates.STATE_3[0])
    else:
        await message.answer("Это не число")
    await next_question(message.from_user.id)


@dp.message_handler(state=TestStates.STATE_3 | TestStates.FINAL_STATE)
async def object_type_question(message: types.Message):
    global link_params
    state = dp.current_state(user=message.from_user.id)
    cur_state = await state.get_state()
    if message.text.isdigit():
        link_params["maxprice"] = message.text
        if cur_state in TestStates.STATE_3:
            await state.set_state(TestStates.STATE_4[0])
    else:
        await message.answer("Это не число")
    await next_question(message.from_user.id)


@dp.message_handler(state=TestStates.STATE_4 | TestStates.FINAL_STATE)
async def object_type_question(message: types.Message):
    global link_params
    state = dp.current_state(user=message.from_user.id)
    cur_state = await state.get_state()
    if message.text.isdigit():
        link_params["foot_min"] = message.text
        if cur_state in TestStates.STATE_4:
            await state.set_state(TestStates.STATE_5[0])
    else:
        await message.answer("Это не число")
    await next_question(message.from_user.id)


@dp.message_handler(state=TestStates.STATE_5 | TestStates.FINAL_STATE)
async def object_type_question(message: types.Message):
    global link_params
    state = dp.current_state(user=message.from_user.id)
    cur_state = await state.get_state()
    if message.text.isdigit():
        link_params["mintarea"] = message.text
        if cur_state in TestStates.STATE_5:
            await state.set_state(TestStates.STATE_6[0])
    else:
        await message.answer("Это не число")
    await next_question(message.from_user.id)


@dp.message_handler(state=TestStates.STATE_6 | TestStates.FINAL_STATE)
async def object_type_question(message: types.Message):
    global link_params
    state = dp.current_state(user=message.from_user.id)
    cur_state = await state.get_state()
    if message.text.isdigit():
        link_params["minkarea"] = message.text
        if cur_state in TestStates.STATE_6:
            await state.set_state(TestStates.STATE_7[0])
    else:
        await message.answer("Это не число")
    await next_question(message.from_user.id)


@dp.message_handler(state=TestStates.STATE_7 | TestStates.FINAL_STATE)
async def object_type_question(message: types.Message):
    global link_params
    state = dp.current_state(user=message.from_user.id)
    cur_state = await state.get_state()
    if message.text.isdigit():
        link_params["maxkarea"] = message.text
        if cur_state in TestStates.STATE_7:
            await state.set_state(TestStates.FINAL_STATE[0])
    else:
        await message.answer("Это не число")
    await next_question(message.from_user.id)


@dp.callback_query_handler(lambda c: c.data == "btn11", state=TestStates.FINAL_STATE)
async def object_type_question(callback_query: types.CallbackQuery):
    global link_params
    state = dp.current_state(user=callback_query.from_user.id)
    link = await make_link()
    link_params = {}
    await state.set_state(None)
    await bot.send_message(callback_query.from_user.id, f"Твоя ссылка: {link}")
    await count_cian(callback_query.from_user.id, link)


@dp.callback_query_handler(lambda c: c.data == "btn12", state=TestStates.FINAL_STATE)
async def object_type_question(callback_query: types.CallbackQuery):
    global link_params
    link_params = {}
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(TestStates.STATE_0[0])
    await bot.send_message(callback_query.from_user.id, "Давай попробуем заново")
    await next_question(callback_query.from_user.id)


@dp.message_handler(regexp=r"https://www.cian.ru/.*")
async def start_cian(message: types.Message):
    await count_cian(message.from_user.id, message.text)
