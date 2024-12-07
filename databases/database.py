import sqlite3


def set_pole(username: str, name: str, value):
    con = sqlite3.connect("databases/db.sqlite")
    cur = con.cursor()
    cur.execute(
        f"""UPDATE Users
            SET {name} = {repr(value)}
            WHERE username = '{username}'"""
    )

    con.commit()
    con.close()


def add_user(username: str):
    con = sqlite3.connect("databases/db.sqlite")
    cur = con.cursor()

    cur.execute(
        f"""INSERT INTO Users(username)
                VALUES('{username}')"""
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
            SET in_game = ?
            WHERE username = '{username}'""",
        (in_game,),
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
