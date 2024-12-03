import sqlite3


def add_user(username: str, chat_id: int, last_message_id: int):
    fl = username in get_row("username")
    con = sqlite3.connect("databases/db.sqlite")
    cur = con.cursor()
    if fl:
        cur.execute(
            f"""UPDATE Users
            SET last_message_id = {last_message_id},
                chat_id = {chat_id}
            WHERE username = '{username}'"""
        )
    else:
        cur.execute(
            f"""INSERT INTO Users(username, chat_id, last_message_id)
                VALUES('{username}', {chat_id}, {last_message_id})"""
        )
    con.commit()
    con.close()


def get_row(name: str):
    con = sqlite3.connect("databases/db.sqlite")
    cur = con.cursor()
    result = cur.execute(
        f"""SELECT {name}
            FROM Users"""
    ).fetchall()
    con.close()
    return next(zip(*result))


def set_in_game(username: str, in_game: int):
    con = sqlite3.connect("databases/db.sqlite")
    cur = con.cursor()
    cur.execute(
        f"""UPDATE Users
            SET in_game = {in_game}
            WHERE username = '{username}'"""
    )
    con.commit()
    con.close()


def get_res(username: str, name: str):
    con = sqlite3.connect("databases/db.sqlite")
    cur = con.cursor()
    result = cur.execute(
        f"""SELECT {name}
            FROM Users
            WHERE username = '{username}'"""
    ).fetchone()
    con.close()
    return result[0]
