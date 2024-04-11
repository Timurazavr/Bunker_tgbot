from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
)
from lexicon.lexicon import LEXICON
from keyboards.pagination_kb import create_keyb, create_keyb_rol
from services.services import sp, sl, rols, sl_rol
from secret import API_TOKEN

router = Router()
txt = open(
    "C:\\Users\\timur\\Desktop\\Codes\\Mafia-main\\Роли.txt", "r", encoding="utf8"
).read()
bot = Bot(token=API_TOKEN, parse_mode="HTML")


@router.message(CommandStart())
async def process_start_command(message: Message):
    name = message.from_user.first_name
    await message.answer(
        LEXICON[message.text].format(name if name else "Игрок"),
        reply_markup=create_keyb("role", "full"),
    )


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(txt)


@router.callback_query(F.data.in_(("role", "leave")))
async def onl(callback: CallbackQuery):
    if (
        callback.from_user.username,
        callback.from_user.id,
        callback.message.message_id,
    ) in sp:
        sp.remove(
            (
                callback.from_user.username,
                callback.from_user.id,
                callback.message.message_id,
            )
        )
    await callback.message.edit_text(
        text=LEXICON["role_lobby"], reply_markup=create_keyb("join")
    )


@router.callback_query(F.data == "join")
async def process_offline_press(callback: CallbackQuery):
    sp.append(
        (
            callback.from_user.username,
            callback.from_user.id,
            callback.message.message_id,
        )
    )
    if len(sp) == 1:
        await callback.message.edit_text(
            text=LEXICON["lider"].format(len(sp) - 1),
            reply_markup=create_keyb("leave", "clear", "raspr", "start"),
        )
    else:
        await callback.message.edit_text(
            text=LEXICON["in_lobby"].format(callback.data),
            reply_markup=create_keyb("leave", "jim"),
        )


@router.callback_query(F.data.in_(("leavel")))
async def process_offline_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON["lider"],
        reply_markup=create_keyb("leave", "clear", "raspr", "start"),
    )


@router.callback_query(F.data == "raspr")
async def process_offline_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON["lider"],
        reply_markup=create_keyb_rol(),
    )


@router.callback_query(F.data[0].in_("-+"))
async def process_offline_press(callback: CallbackQuery):
    sl[callback.data[1:]] += 1 if callback.data[0] == "+" else -1
    await callback.message.edit_reply_markup(
        reply_markup=create_keyb_rol(),
    )


@router.callback_query(F.data == "jim")
async def process_offline_press(callback: CallbackQuery):
    await callback.answer(
        f"Ваша роль: {LEXICON[sl_rol.get(callback.from_user.id)][:-3]}",
        show_alert=True,
    )


@router.callback_query(F.data == "start")
async def process_offline_press(callback: CallbackQuery):
    if sum(sl.values()) != len(sp) - 1:
        await callback.message.answer(text="Кол-во ролей неравно кол-ву игроков!")
    else:
        sl_rol.clear()
        for igr, rol in zip(sp[1:], rols(sl)):
            sl_rol[igr[1]] = rol
    await callback.answer()


@router.callback_query(F.data == "clear")
async def process_offline_press(callback: CallbackQuery):
    for j in sp:
        await bot.edit_message_text(
            text=LEXICON["role_lobby"],
            reply_markup=create_keyb("join"),
            chat_id=j[1],
            message_id=j[2],
        )
    sp.clear()
