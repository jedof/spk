from datetime import datetime
from sqlalchemy import (
    orm,
    Integer,
    String
)
from sqlalchemy.types import DateTime
from pydantic import BaseModel, ConfigDict


class Base(orm.DeclarativeBase):
    pass


class DbInterviewTickets(Base):
    __tablename__ = "interview_tickets"

    user_id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True)
    tg_user_id: orm.Mapped[int] = orm.mapped_column(Integer, nullable=False, unique=True)
    name: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    phone_number: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    date: orm.Mapped[datetime] = orm.mapped_column(DateTime, nullable=False)



class BaseConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class InterviewBaseTicket(BaseConfig):
    name: str
    phone_number: str
    date: datetime


class InterviewTicket(InterviewBaseTicket):
    user_id: int
    tg_user_id: int 
