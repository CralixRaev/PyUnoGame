from os import PathLike
import sqlite3
from utilities import password_utility


class Authorization:
    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def register(self, username: str, password: str):
        hashed_password = password_utility.hash_password(password)
        self.cursor.execute("""INSERT INTO users(name, password) VALUES(?, ?)""",
                            (username, hashed_password))
        self.db.commit()

    def __del__(self):
        self.db.close()
