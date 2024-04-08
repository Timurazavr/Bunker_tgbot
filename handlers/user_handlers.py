from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
)
from lexicon.lexicon import LEXICON
from keyboards.pagination_kb import create_keyb, create_krest_nol
from databases.database import users_db, user_dict_template
from services.services import table_priv
from databases.database import get_in_admins

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    if get_in_admins(message.from_user.id):
        await message.answer("Привет Админ")
    if 2:
        name = message.from_user.first_name
        await message.answer(
            LEXICON[message.text].format(name if name else "Игрок"),
            reply_markup=create_keyb("role", "full"),
        )


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.callback_query(F.data == "role")
async def process_offline_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON["role_lobby"], reply_markup=create_keyb("k1", "k2", "k3")
    )


