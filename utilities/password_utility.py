import bcrypt  # bcrypt - надежнее SHA512, так что используем его


# Нет, это не лишнее, хеширование тут реализовать элементарно,
# зато в базе не будут храниться пароли в открытом виде

# Правда есть ещё одна уязвимость - все данные передаются серверу в открытом виде.
# Зато, если переписать весь нетворкинг, это можно легко исправить
# (к примеру, хотя бы подписывать объекты с помощью HMAC, что бы никто нам чужой код не подсунул)

# а может и вообще передавать всю авторизацию через bson)) (шучу, но для авторизации это как вариант)
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
