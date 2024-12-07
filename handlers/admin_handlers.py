from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
)
from lexicon.lexicon import LEXICON
from secret import ADMIN_IDS
from keyboards.pagination_kb import create_keyb
from databases.database import get_row

router = Router()


@router.message(F.text.startswith("/code"), F.from_user.id.in_(ADMIN_IDS))
async def process_start_command(message: Message):
    a = eval(message.text[6:])
    await message.answer(text=str(a))


@router.message(F.text.startswith("/clear"), F.from_user.id.in_(ADMIN_IDS))
async def process_offline_press(message: Message, bot: Bot):
    for j in sp:
        await bot.edit_message_text(
            text=LEXICON["role_lobby"],
            reply_markup=create_keyb("join", "down"),
            chat_id=j[1],
            message_id=j[2],
        )
    sp.clear()
