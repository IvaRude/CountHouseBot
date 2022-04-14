from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn1 = InlineKeyboardButton("Да", callback_data="btn1")
btn2 = InlineKeyboardButton("Нет", callback_data="btn2")

keyboard1 = InlineKeyboardMarkup().add(btn1, btn2)

btn3 = InlineKeyboardButton("Да, на двушку", callback_data="btn3")
btn4 = InlineKeyboardButton("Да, на трешку", callback_data="btn4")
btn5 = InlineKeyboardButton("Нет", callback_data="btn5")

keyboard2 = InlineKeyboardMarkup().add(btn3, btn4, btn5)

btn6 = InlineKeyboardButton("Вторичка", callback_data="btn6")
btn7 = InlineKeyboardButton("Новостройка", callback_data="btn7")
btn8 = InlineKeyboardButton("И то, и то", callback_data="btn8")

object_type_keyboard = InlineKeyboardMarkup().add(btn6, btn7, btn8)

btn9 = InlineKeyboardButton("Двушка", callback_data="btn9")
btn10 = InlineKeyboardButton("Трешка", callback_data="btn10")
btn9_10 = InlineKeyboardButton("И то, и то", callback_data="btn9_10")

room_keyboard = InlineKeyboardMarkup().add(btn9, btn10)

btn11 = InlineKeyboardButton("Да", callback_data="btn11")
btn12 = InlineKeyboardButton("Нет", callback_data="btn12")

final_keyboard = InlineKeyboardMarkup().add(btn11, btn12)

# btn13 = InlineKeyboardButton("Тип жилья", callback_data="btn13")
# btn14 = InlineKeyboardButton("Количество комнат", callback_data="btn14")
# btn15 = InlineKeyboardButton("Цена от", callback_data="btn15")
# btn16 = InlineKeyboardButton("Цена до", callback_data="btn16")
# btn17 = InlineKeyboardButton("Время до метро", callback_data="btn17")
# btn18 = InlineKeyboardButton("Общая площадь от", callback_data="btn18")
# btn19 = InlineKeyboardButton("Кухня от", callback_data="btn19")
# btn20 = InlineKeyboardButton("Кухня до", callback_data="btn20")
# btn21 = InlineKeyboardButton("", callback_data="btn21")
#
# requestion_keyboard = InlineKeyboardMarkup().add(btn13, btn14, btn15, btn16,
#                                                  btn17, btn18, btn19, btn20)
