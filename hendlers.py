from aiogram.filters import Command, StateFilter
from aiogram import Router, types

router = Router()


class RequestForm:
    name = "name"
    phone = "phone"
    time = "time"
    

@router.message(Command("start"))
async def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Информация", "Подать заявку"]
    keyboard.add(*buttons)
    await message.reply("Привет! Это Студенческий Парламентский Клуб РУДН. Чем могу помочь?", reply_markup=keyboard)


@router.message(lambda message: message.text == "Информация")
async def send_info(message):
    await message.reply("Здесь вы можете получить информацию об организации.")



@router.message(lambda message: message.text == "Подать заявку")
async def request_info(message):
    await message.reply("Для подачи заявки, пожалуйста, укажите ваше ФИО:")
    await RequestForm.name.set()


@router.message(StateFilter(RequestForm.name))
async def process_name(message, state):
    async with state.proxy() as data:
        data[RequestForm.name] = message.text
    await message.reply("Теперь укажите ваш номер телефона:")
    await RequestForm.phone.set()


@router.message(StateFilter(RequestForm.phone))
async def process_phone(message, state):
    async with state.proxy() as data:
        data[RequestForm.phone] = message.text

    await message.reply("Наконец, укажите желаемое время собеседования:")
    await RequestForm.time.set()


@router.message(StateFilter(RequestForm.time))
async def process_time(message, state):
    async with state.proxy() as data:
        data[RequestForm.time] = message.text
        await message.reply("Спасибо за заявку! Мы свяжемся с вами в ближайшее время.")
    await state.finish()