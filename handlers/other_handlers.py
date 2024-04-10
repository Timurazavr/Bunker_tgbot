from aiogram import Router
from aiogram.types import Message, CallbackQuery

router: Router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    await message.answer(text=f"Это эхо! {message.text}")


@router.callback_query()
async def process_offline_press(callback: CallbackQuery):
    await callback.answer()
