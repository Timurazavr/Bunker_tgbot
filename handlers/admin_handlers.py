from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
)
from lexicon.lexicon import LEXICON
from services.services import sp, sl_rol, sl

router = Router()


@router.message(F.text.startswith("/code"), F.from_user.id == 5050670131)
async def process_start_command(message: Message):
    a = eval(message.text[6:])
    await message.answer(text=str(a))
