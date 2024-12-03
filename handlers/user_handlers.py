from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, FSInputFile
from lexicon.lexicon import LEXICON
from keyboards.pagination_kb import create_keyb
from services.services import sp, get_roles, rooms, Room, Player, generate_id
from aiogram.exceptions import TelegramBadRequest
from databases.database import get_row, add_user, set_in_game, get_res

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    name = message.from_user.first_name
    message_id = (
        await message.answer(
            LEXICON["/start"].format(name if name else "Игрок"),
            reply_markup=create_keyb("role", "full", "download_rules"),
        )
    ).message_id
    add_user(message.from_user.username, message.chat.id, message_id)


@router.callback_query(F.data == "role")
async def process_role_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON["role_lobby"],
        reply_markup=create_keyb(*(str(i) for i in rooms), "create", "down"),
    )


@router.callback_query(F.data == "download_rules")
async def process_download_rules(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer_document(FSInputFile("Rules.pdf"))


@router.callback_query(F.data == "create")
async def process_create_callback(callback: CallbackQuery):
    id_room = generate_id()
    rooms[id_room] = Room(Player(callback.from_user.username))
    set_in_game(callback.from_user.username, id_room)
    await callback.message.edit_text(
        text=LEXICON["lider"],
        reply_markup=create_keyb("leave", "clear", "start"),
    )


@router.callback_query(F.data == "down")
async def process_down_callback(callback: CallbackQuery):
    name = callback.message.from_user.first_name
    await callback.message.edit_text(
        text=LEXICON["/start"].format(name if name else "Игрок"),
        reply_markup=create_keyb("role", "full", "download_rules"),
    )


@router.callback_query(F.data == "leave")
async def process_leave_callback(callback: CallbackQuery):
    await callback.answer()
    # if all((callback.from_user.username, callback.from_user.id) != i[:2] for i in sp):
    #     sp.append(
    #         (
    #             callback.from_user.username,
    #             callback.from_user.id,
    #             callback.message.message_id,
    #         )
    #     )
    # if len(sp) == 1:
    #     await callback.message.edit_text(
    #         text=LEXICON["lider"],
    #         reply_markup=create_keyb("leave", "clear", "start"),
    #     )
    # else:
    #     await callback.message.edit_text(
    #         text=LEXICON["in_lobby"],
    #         reply_markup=create_keyb("leave"),
    #     )


@router.callback_query(F.data == "clear")
async def process_clear_callback(callback: CallbackQuery, bot: Bot):
    id_room = get_res(callback.from_user.username, "in_game")
    for i in rooms[id_room].players:
        await bot.edit_message_text(
            text=LEXICON["role_lobby"],
            reply_markup=create_keyb(
                *(str(j) for j in rooms if j != id_room), "create", "down"
            ),
            chat_id=get_res(i.username, "chat_id"),
            message_id=get_res(i.username, "last_message_id"),
        )
    del rooms[id_room]


@router.callback_query(F.data == "join")
async def process_offline_press(callback: CallbackQuery, bot: Bot):
    id_room = get_res(callback.from_user.username, "in_game")
    print(get_roles(len(rooms[id_room])))
    # await bot.edit_message_text(
    #     text=LEXICON["role_lobby"],
    #     reply_markup=create_keyb(
    #         *(str(j) for j in rooms if j != id_room), "create", "down"
    #     ),
    #     chat_id=get_res(i.username, "chat_id"),
    #     message_id=get_res(i.username, "last_message_id"),
    # )


@router.callback_query(F.data == "start")
async def process_offline_press(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    res = get_roles(len(sp))
    for i in range(len(res)):
        await bot.i(
            text=LEXICON["role_lobby"],
            reply_markup=create_keyb("join", "down"),
            chat_id=sp[i][1],
        )


# @router.message(Command("clear"))
# async def cmd_clear(message: Message, bot: Bot) -> None:
#     try:
#         # Все сообщения, начиная с текущего и до первого (message_id = 0)
#         for i in range(message.message_id, 0, -1):
#             await bot.delete_message(message.from_user.id, i)
#     except TelegramBadRequest as ex:
#         # Если сообщение не найдено (уже удалено или не существует),
#         # код ошибки будет "Bad Request: message to delete not found"
#         if ex.message == "Bad Request: message to delete not found":
#             print("Все сообщения удалены")
