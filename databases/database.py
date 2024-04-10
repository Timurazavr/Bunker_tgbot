user_dict_template: dict = {"hod": True, "sost": False}
users_db: dict = {}
# from mysql.connector import connect

# connection = connect(
#     host="localhost",
#     user="root",
#     password="timati110309_",
#     database="Telebot",
# )


# def get_in_admins(id: int):
#     a = """SELECT user_id FROM admins"""
#     with connection.cursor() as cursor:
#         cursor.execute(a)
#         result = cursor.fetchall()
#     return (id,) in result

