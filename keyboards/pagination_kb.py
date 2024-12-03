from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


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
