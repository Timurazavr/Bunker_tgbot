from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_keyb(*buttons: str) -> InlineKeyboardMarkup:
    keyb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyb.row(
        *[
            InlineKeyboardButton(text=LEXICON.get(b, b), callback_data=b)
            for b in buttons
        ]
    )
    return keyb.as_markup()


def create_krest_nol() -> InlineKeyboardMarkup:
    keyb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyb.row(
        *[InlineKeyboardButton(text="-", callback_data=str(b)) for b in range(1, 10)],
        InlineKeyboardButton(text="Закончить игру", callback_data="konch"),
        width=3
    )
    return keyb.as_markup()
