from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router, types, F
from db.session import get_db_session
from db import db
from db.models import InterviewBaseTicket
from filters import FullNameFilter
from aiogram_calendar import DialogCalendar, DialogCalendarCallback
from aiogram.filters.callback_data import CallbackData
from keyboards import (
    menu_keyboard, 
    finish_keyboard,
    hours_kb_builder,
    minutes_kb_builder
)


router = Router()


class RequestForm(StatesGroup):
    name = State()
    phone = State()
    date = State()
    choosing_hours = State()
    choosing_minutes = State()    


@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Это Студенческий Парламентский Клуб РУДН. Чем могу помочь?", reply_markup=menu_keyboard)


@router.message(F.text == "Информация")
async def send_info(message: types.Message):
    await message.reply("Направления деятельности СПК РУДН:\n"
                        "💬 Участие в мероприятиях/конференциях/диалогах с государственными лицами разных уровней от местного до федерального значения;\n"
                        "🙋 Развитие коммуникативных навыков,\n"
                        "посредством участия в дебатах;\n"
                        "🚀 Внедрение во внутреннюю кухню молодежной политики с её последовательным изучением от анализа законотворческого процесса до понимания исполнительных механизмов государства;\n"
                        "🔥 Организация интересных лекций и тренингов от популярных личностей.\n\n"
                        "Проекты реализуемые в рамках СПК:\n"
                        "• Школа молодого законотворца;\n"
                        "• Один день с депутатом;\n"
                        "• Управленческие поединки;\n"
                        "• Дебат-нокаут;\n"
                        "• Лига дебатов;\n"
                        "• Не диванные критики;\n"
                        "• Деловые игры;\n"
                        "• Полит. кухня.\n\n"
                        "Возможности от участия в проектах СПК:\n"
                        "🏆 Стажировки в Правительстве Москвы, которые позволят стать частью государственной структуры страны;\n"
                        "💼 Знакомства и контакты с государственными лицами для построения своего карьерного пути под их руководством;\n"
                        "🧠 Развитие деловых качеств, которые нужны молодому политику для реализации своих целей;\n"
                        "🗣 Прокачка ораторских навыков, без которых невозможно правильно и корректно донести свою точку зрения до слушателей / электората.\n\n"
                        "Студенческие парламентские клубы – это молодежное объединение студентов, которые совершенствуют свои навыки, следят за общественно – политической жизнью города, страны, развивают студенческое самоуправление.\n\n"
                        "СПК – это проект Правительства Москвы, который был запущен в 2017 году в 13 вузах столицы, на сегодняшний день в проекте принимают участие 53 вузов. За 7 года работы проекта было организованно около 200 встреч с депутатами и представителями государственных учреждений.")


@router.message(StateFilter(None), F.text.in_(["Подать заявку", "Изменить"]))
async def request_info(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Для подачи заявки, пожалуйста, укажите ваше ФИО:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RequestForm.name)


@router.message(StateFilter(RequestForm.name), F.text, FullNameFilter())
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Отправить контакт", request_contact=True))
    await message.reply("Теперь укажите ваш номер телефона:", reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True))
    await state.set_state(RequestForm.phone)


@router.message(StateFilter(RequestForm.name), F.text)
async def process_wrong_name(message: types.Message, state: FSMContext):
    await message.reply("Пожалуйста, укажите ваше ФИО через пробел:", reply_markup=types.ReplyKeyboardRemove())


@router.message(StateFilter(RequestForm.phone), F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    if message.contact.user_id == message.from_user.id:
        await state.update_data(phone_number=message.contact.phone_number)
        await message.reply("Наконец, укажите желаемое время собеседования:", reply_markup=await DialogCalendar().start_calendar(year=2024, month=6))
        await state.set_state(RequestForm.date)


@router.callback_query(DialogCalendarCallback.filter(), StateFilter(RequestForm.date))
async def process_dialog_calendar(callback_query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date=date)
        await callback_query.message.answer("Выбери часы", reply_markup=hours_kb_builder.as_markup())
        await state.set_state(RequestForm.choosing_hours)


@router.callback_query(RequestForm.choosing_hours, F.data.startswith("hours_"))
async def hours_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(hour=callback.data.split("_")[1])
    await callback.answer()
    await callback.message.edit_text("Выберите минуты", reply_markup=minutes_kb_builder.as_markup())
    await state.set_state(RequestForm.choosing_minutes)


@router.callback_query(RequestForm.choosing_minutes, F.data.startswith("minutes_"))
async def minutes_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(minutes=callback.data.split("_")[1])
    await callback.answer()
    user_data = await state.get_data()
    model_user_data = InterviewBaseTicket(**user_data)
    model_user_data.date = model_user_data.date.replace(hour=int(user_data["hour"]), minute=int(user_data["minutes"]))
    await state.update_data(date=model_user_data.date)
    print(model_user_data)
    await callback.message.edit_text(
        f"Вы выбрали"
        f"\nИмя: {model_user_data.name}"
        f"\nТелефон: {model_user_data.phone_number}"
        f"\nДата: {model_user_data.date.strftime('%d.%m %H:%M')}",
        reply_markup=None
    )
    await callback.message.answer("все ли верно?", reply_markup=finish_keyboard)
    await state.set_state(state=None)


@router.message(F.text == "Все верно")
async def process_time(message: types.Message, state: FSMContext):
    async with get_db_session() as session:
        user_info = await db.db_get_user_data(session, message.from_user.id)
        if user_info:
            result = await db.db_update_user(session, state, message)
            if not result:
                await message.reply("Произошла ошибка. Попробуйте позже", reply_markup=types.ReplyKeyboardRemove())
                return
            await message.reply("ваша заявка была изменена", reply_markup=menu_keyboard)
        else:
            result = await db.db_add_user(session, state, message)
            if not result:
                await message.reply("Произошла ошибка. Попробуйте позже", reply_markup=types.ReplyKeyboardRemove())
                return
            await message.reply("ваша заявка была принята", reply_markup=menu_keyboard)
    await state.clear()
