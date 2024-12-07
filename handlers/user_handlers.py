from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, FSInputFile
from lexicon.lexicon import LEXICON
from keyboards.pagination_kb import create_keyb
from services.services import (
    get_roles,
    rooms,
    Room,
    Player,
    generate_id,
    rounds_dict,
    get_kat,
)
from databases.database import get_row, add_user, set_in_game, get_res, set_pole
from random import shuffle
from os import listdir

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    if message.from_user.username in get_row("username"):
        nickname = get_res(message.from_user.username, "nickname")
        message_id = (
            await message.answer(
                LEXICON["/start"].format(nickname),
                reply_markup=create_keyb("role", "full", "download_rules"),
            )
        ).message_id
        set_pole(message.from_user.username, "last_message_id", message_id)
    else:
        await message.answer(
            LEXICON["/startfirst"],
        )


@router.message(Command("nickname"))
async def process_nickname_command(message: Message):
    nickname = message.text[10:]
    if 1 <= len(nickname) <= 20:
        if message.from_user.username not in get_row("username"):
            add_user(message.from_user.username)
        set_pole(message.from_user.username, "chat_id", message.chat.id)
        set_pole(message.from_user.username, "nickname", nickname)
        await message.answer(LEXICON["/nickname"])
    else:
        await message.answer(LEXICON["error"])


@router.callback_query(F.data == "role")
async def process_role_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON["role_lobby"],
        reply_markup=create_keyb(*rooms, "create", "down"),
    )


@router.callback_query(F.data == "download_rules")
async def process_download_rules(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer_document(FSInputFile("Rules.pdf"))


@router.callback_query(F.data.in_(rooms))
async def process_connect_press(callback: CallbackQuery, bot: Bot):
    set_in_game(callback.from_user.username, callback.data)
    rooms[callback.data].players.append(Player(callback.from_user.username))
    await callback.message.edit_text(
        text=LEXICON["wait"],
        reply_markup=create_keyb("leave"),
    )
    await bot.edit_message_text(
        text=LEXICON["lider"].format(callback.data, len(rooms[callback.data])),
        reply_markup=create_keyb("leave", "clear", "start"),
        chat_id=get_res(rooms[callback.data].players[0].username, "chat_id"),
        message_id=get_res(rooms[callback.data].players[0].username, "last_message_id"),
    )


@router.callback_query(F.data == "create")
async def process_create_callback(callback: CallbackQuery):
    id_room = generate_id()
    rooms[id_room] = Room(Player(callback.from_user.username))
    set_in_game(callback.from_user.username, id_room)
    await callback.message.edit_text(
        text=LEXICON["lider"].format(id_room, 1),
        reply_markup=create_keyb("leave", "clear", "start"),
    )


@router.callback_query(F.data == "down")
async def process_down_callback(callback: CallbackQuery):
    nickname = get_res(callback.from_user.username, "nickname")
    await callback.message.edit_text(
        LEXICON["/start"].format(nickname),
        reply_markup=create_keyb("role", "full", "download_rules"),
    )


@router.callback_query(F.data == "leave")
async def process_leave_callback(callback: CallbackQuery, bot: Bot):
    room_id = get_res(callback.from_user.username, "in_game")
    for i in range(len(rooms[room_id])):
        if rooms[room_id].players[i].username == callback.from_user.username:
            del rooms[room_id].players[i]
            break
    if not len(rooms[room_id]):
        del rooms[room_id]
    else:
        await bot.edit_message_text(
            text=LEXICON["lider"].format(room_id, len(rooms[room_id])),
            reply_markup=create_keyb("leave", "clear", "start"),
            chat_id=get_res(rooms[room_id].players[0].username, "chat_id"),
            message_id=get_res(rooms[room_id].players[0].username, "last_message_id"),
        )
    set_in_game(callback.from_user.username, None)
    await callback.message.edit_text(
        text=LEXICON["role_lobby"],
        reply_markup=create_keyb(*rooms, "create", "down"),
    )


@router.callback_query(F.data == "clear")
async def process_clear_callback(callback: CallbackQuery, bot: Bot):
    id_room = get_res(callback.from_user.username, "in_game")
    for i in rooms[id_room].players:
        await bot.edit_message_text(
            text=LEXICON["role_lobby"],
            reply_markup=create_keyb(
                *(j for j in rooms if j != id_room), "create", "down"
            ),
            chat_id=get_res(i.username, "chat_id"),
            message_id=get_res(i.username, "last_message_id"),
        )
        set_in_game(i.username, None)
    del rooms[id_room]


@router.callback_query(F.data == "start")
async def process_start_press(callback: CallbackQuery, bot: Bot):
    id_room = get_res(callback.from_user.username, "in_game")
    kat = get_kat()
    rooms[id_room].bunk = ["JPG\\Бункер" + "\\" + x for x in listdir("JPG\\Бункер")]
    shuffle(rooms[id_room].bunk)
    bunk = rooms[id_room].bunk.pop()
    for i, rol in zip(rooms[id_room].players, get_roles(len(rooms[id_room].players))):
        specifications = [j[j.rfind("\\") + 1 :].rstrip(".jpg").lower() for j in rol]
        i.open_specifications.append(specifications[0])
        i.specifications.extend(specifications[1:])

        for j in rol:
            await bot.send_photo(
                photo=FSInputFile(j),
                chat_id=get_res(i.username, "chat_id"),
            )
        await bot.send_photo(
            photo=FSInputFile(kat),
            chat_id=get_res(i.username, "chat_id"),
        )
        await bot.send_photo(
            photo=FSInputFile(bunk),
            chat_id=get_res(i.username, "chat_id"),
        )

    result = ""
    for i in rooms[id_room].players:
        nickname = get_res(i.username, "nickname")
        result += nickname + ":" + "\n" + i.open_specifications[0] + "\n\n"
        print(repr(result))

    for i in rooms[id_room].players:
        message_id = (
            await bot.send_message(
                text=result,
                chat_id=get_res(i.username, "chat_id"),
            )
        ).message_id
        set_pole(i.username, "last_message_id", message_id)

    rooms[id_room].active_player = rooms[id_room].players[0]

    await bot.edit_message_text(
        text=result,
        reply_markup=create_keyb(*rooms[id_room].players[0].specifications),
        chat_id=get_res(rooms[id_room].players[0].username, "chat_id"),
        message_id=get_res(rooms[id_room].players[0].username, "last_message_id"),
    )


@router.callback_query(
    lambda x: x.data
    in rooms[get_res(x.from_user.username, "in_game")].active_player.specifications
)
async def process_open_spec_press(callback: CallbackQuery, bot: Bot):
    id_room = get_res(callback.from_user.username, "in_game")
    for player in rooms[id_room].players:
        if player.username == callback.from_user.username:
            break
    player.open_specifications.append(callback.data)
    player.specifications.remove(callback.data)

    result = ""
    for i in rooms[id_room].players:
        nickname = get_res(i.username, "nickname")
        result += nickname + ":" + "\n" + "\n".join(i.open_specifications) + "\n\n"

    for i in rooms[id_room].players:
        await bot.edit_message_text(
            text=result,
            chat_id=get_res(i.username, "chat_id"),
            message_id=get_res(i.username, "last_message_id"),
        )
    rooms[id_room].next_active_player()
    await bot.edit_message_text(
        text=result,
        reply_markup=create_keyb(*rooms[id_room].active_player.specifications),
        chat_id=get_res(rooms[id_room].active_player.username, "chat_id"),
        message_id=get_res(rooms[id_room].active_player.username, "last_message_id"),
    )
