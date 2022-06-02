import bcrypt
from sqlalchemy import create_engine

def init():
    engine = create_engine('sqlite:///crypto.db')
    return engine

def create_user(username, password):
    engine = init()
    try:
        engine.execute(f"""
            INSERT INTO users (
                username,
                password,
                created
            ) VALUES (
                '{username}',
                '{password}',
                DATETIME('now')
            );"""
        )
        return True
    except:
        return False

def auth(username, password):
    engine = init()
    res = engine.execute(f"SELECT password FROM users WHERE username='{username}' LIMIT 1;").fetchall()
    if len(res) != 1:
        return False
    else:
        hashed_password = res[0][0].encode('utf-8')
        return bcrypt.checkpw(password, hashed_password)


def store_price(currency_name, currency_value):
    return True
