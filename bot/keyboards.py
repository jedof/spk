from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


menu_keyboard: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Информация"),
            types.KeyboardButton(text="Подать заявку")
        ]
    ],
    resize_keyboard=True, 
) 


finish_keyboard: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Все верно"),
            types.KeyboardButton(text="Изменить")
        ]
    ],
    resize_keyboard=True, 
    one_time_keyboard=True
) 


hours_kb_builder = InlineKeyboardBuilder()
for i in range(9, 19):
    hours_kb_builder.row(
        types.InlineKeyboardButton(
            text=f"{i}:00",
            callback_data=f"hours_{i}",
        )
    )


minutes_kb_builder = InlineKeyboardBuilder()
for i in range(0, 60, 10):
    minutes_kb_builder.row(
        types.InlineKeyboardButton(
            text=str(i) if i > 0 else "00",
            callback_data=f"minutes_{str(i) if i > 0 else '00'}",
        )
    )