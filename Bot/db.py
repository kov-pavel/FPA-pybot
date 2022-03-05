import sqlite3
import os

from Bot.config import WATERMARKS


class Database:
    DB_NAME = "users.db"

    def __enter__(self):
        self.__connection = sqlite3.connect(self._get_path())
        self.__init_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.close()

    def _get_path(self) -> str:
        path = os.path.realpath(__file__)
        path = path.removesuffix(os.path.basename(__file__))
        path = os.path.join(path, self.DB_NAME)
        path = r"{}".format(path)
        return path

    def __init_table(self) -> None:
        self.__connection.execute("""CREATE TABLE IF NOT EXISTS users 
                                (id BIGINT,
                                word VARCHAR(30),
                                is_admin BOOLEAN,
                                name VARCHAR(30),
                                UNIQUE(id)
                                );""")
        self.__connection.commit()

    def get_watermark_type(self, user_id: int) -> str:
        result = self.__connection.execute(f"""SELECT word FROM users WHERE id={user_id};""").fetchone()
        return result[0] if result is not None else None

    def set_new_word(self, user_id: int, word: str) -> None:
        self.__connection.execute(f"""UPDATE users SET word = '{word}' WHERE id = {user_id};""")
        self.__connection.commit()

    def close(self) -> None:
        self.__connection.close()

    def is_admin(self, user_id: int) -> bool:
        admin = self.__connection.execute(f"""SELECT is_admin FROM users WHERE id={user_id};""").fetchone()
        return admin[0] if admin is not None else False

    def is_user(self, user_id: int) -> bool:
        user = self.__connection.execute(f"""SELECT is_admin FROM users WHERE id={user_id};""").fetchone()
        return user is not None

    def add_new_user(self, user_id: int, is_admin: bool, name: str) -> None:
        self.__connection.execute(
            f"""INSERT OR REPLACE INTO users (id, word, is_admin, name)
                VALUES ({user_id}, '{next(iter(WATERMARKS.keys()))}', {is_admin}, '{name}');""")
        self.__connection.commit()

    def delete_user(self, user_id: int) -> None:
        self.__connection.execute(
            f"""DELETE FROM users WHERE id = {user_id}""")
        self.__connection.commit()

    def get_all_users(self) -> list:
        return self.__connection.execute("""SELECT id, is_admin, name FROM users""").fetchall()
