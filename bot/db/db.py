from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, text, exc
from aiogram.types import Message
from .models import DbInterviewTickets, InterviewTicket
from aiogram.fsm.context import FSMContext


async def db_get_user_data(session: AsyncSession, tg_user_id: int):
    user_data = await session.scalars(
        select(DbInterviewTickets).where(DbInterviewTickets.tg_user_id == tg_user_id)
    )
    user_data = user_data.first()
    if user_data:
        return InterviewTicket.model_validate(user_data)


async def db_add_user(session: AsyncSession, state: FSMContext, message: Message):
    data = await state.get_data()
    try:
        await session.execute(
            insert(DbInterviewTickets).values(
                tg_user_id=message.from_user.id,
                name=data["name"],
                phone_number=data["phone_number"],
                date=data["date"]
            )
        )
    except exc.SQLAlchemyError as e:
        print(e)
        return False
    return True
        

async def db_update_user(session: AsyncSession, state: FSMContext, message: Message):
    data = await state.get_data()
    try:
        await session.execute(
            update(DbInterviewTickets).where(DbInterviewTickets.tg_user_id == message.from_user.id).values(
                tg_user_id=message.from_user.id,
                name=data["name"],
                phone_number=data["phone_number"],
                date=data["date"]
            )
        )
    except exc.SQLAlchemyError as e:
        print(e)
        return False
    return True
