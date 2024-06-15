from aiogram.filters import BaseFilter
from aiogram import types

import re

full_name = re.compile(r"^(?:(?:[а-яА-Я]+(?:-[а-яА-Я]+)*) ){2,}(?:(?:[а-яА-Я]+(?:-[а-яА-Я]+)*))$")


class FullNameFilter(BaseFilter):
    async def __call__(self, message: types.Message):
        return bool(full_name.match(message.text))