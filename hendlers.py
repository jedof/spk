from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router, types, F


router = Router()


class RequestForm(StatesGroup):
    name = State()
    phone = State()
    time = State()
    

keyboard: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Информация"),
            types.KeyboardButton(text="Подать заявку")
        ]
    ],
    resize_keyboard=True, 
)


@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Это Студенческий Парламентский Клуб РУДН. Чем могу помочь?", reply_markup=keyboard)


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


@router.message(StateFilter(None), F.text == "Подать заявку")
async def request_info(message: types.Message, state: FSMContext):
    await message.reply("Для подачи заявки, пожалуйста, укажите ваше ФИО:")
    await state.set_state(RequestForm.name)


@router.message(StateFilter(RequestForm.name), F.text)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Отправить контакт", request_contact=True))
    await message.reply("Теперь укажите ваш номер телефона:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(RequestForm.phone)


@router.message(StateFilter(RequestForm.phone), F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    if message.contact.user_id == message.from_user.id:
        await state.update_data(phone=message.contact.phone_number)
        await message.reply("Наконец, укажите желаемое время собеседования:")
        await state.set_state(RequestForm.time)


@router.message(StateFilter(RequestForm.time), F.text)
async def process_time(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    print(user_data)
    await message.reply("Спасибо за заявку! Мы свяжемся с вами в ближайшее время.")
    await state.clear()