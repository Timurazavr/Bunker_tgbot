from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
)
from lexicon.lexicon import LEXICON

router = Router()


@router.message(F.text == "sp" | F.from_user.id == 5050670131)
async def process_start_command(message: Message):
    await message.answer(f"s")
