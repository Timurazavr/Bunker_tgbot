from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.services import sl


def create_keyb(*buttons: str) -> InlineKeyboardMarkup:
    keyb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyb.row(
        *[
            InlineKeyboardButton(text=LEXICON.get(b, b), callback_data=b)
            for b in buttons
        ],
        width=1
    )
    return keyb.as_markup()


def create_keyb_rol() -> InlineKeyboardMarkup:
    keyb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in LEXICON["rol"]:
        a = InlineKeyboardButton(text="+", callback_data="+" + i)
        b = InlineKeyboardButton(text=LEXICON[i].format(sl[i]), callback_data=i)
        c = InlineKeyboardButton(text="-", callback_data="-" + i)
        keyb.row(a, b, c, width=3)
    keyb.row(
        InlineKeyboardButton(text=LEXICON["leavel"], callback_data="leavel"), width=3
    )
    return keyb.as_markup()
