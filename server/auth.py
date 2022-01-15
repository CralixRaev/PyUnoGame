from dataclasses import dataclass
from os import PathLike
import sqlite3

from classes.auth.exceptions import WrongCredentials
from classes.auth.user import User
from utilities import password_utility


class Authorization:
    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path)

    def register(self, username: str, password: str) -> User:
        cursor = self.db.cursor()
        hashed_password = password_utility.hash_password(password)
        user = cursor.execute("""INSERT INTO users(name, password) VALUES(?, ?) 
        RETURNING id, name, password""", (username, hashed_password)).fetchone()
        self.db.commit()
        user_id, name, password_hash = user
        return User(user_id, name)

    def login(self, username: str, password: str) -> User:
        cursor = self.db.cursor()
        user = cursor.execute("""SELECT * FROM users WHERE name=?""", (username,)).fetchone()
        if not user:
            raise WrongCredentials("Нет такого пользователя")
        user_id, name, password_hash = user
        if not password_utility.check_password(password, password_hash):
            raise WrongCredentials("Неправильный пароль")
        return User(user_id, name)

    def __del__(self):
        self.db.close()
