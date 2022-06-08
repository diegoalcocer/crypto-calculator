import bcrypt
from matplotlib.pyplot import get
from sqlalchemy import create_engine

# Connects to the local SQLite3 database
def init():
    engine = create_engine('sqlite:///crypto.db')
    return engine

# Inserts a new user into the database
# Password supplied to function is hashed
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

# Validate that the username and password supplied are correct
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

# Given a username, return the user's database ID
def get_user_id(username):
    engine = init()
    res = engine.execute(f"SELECT uid FROM users WHERE username='{username}' LIMIT 1;").fetchall()
    if len(res) < 1:
        return 0
    else:
        result = res[0][0]
        return result

# Retrieve all the wallets for a given username
def get_wallets(username):
    engine = init()
    user_id = get_user_id(username)
    wallets = engine.execute(f"""
    SELECT *
    FROM wallets
    WHERE userid = {user_id}
    """).fetchall()
    return wallets

# Retrive all the wallets in the supplied currency given a username
def get_wallet_by_currency(username, currency):
    engine = init()
    user_id = get_user_id(username)
    wallet = engine.execute(f"""
    SELECT *
    FROM wallets
    WHERE
        userid = {user_id}
        AND currency = '{currency}'
    """).fetchall()
    return wallet

# Add funds to a wallet
def update_wallet(username, balance, currency):
    engine = init()
    user_id = get_user_id(username)
    try:
        # If wallet doesn't exist, then create the wallet with the supplied currency amount
        if len(get_wallet_by_currency(username, currency)) < 1:
                engine.execute(f"""
                    INSERT INTO wallets (
                        userid,
                        currency,
                        balance,
                        created
                    ) VALUES (
                        {user_id},
                        '{currency}',
                        {balance},
                        DATETIME('now')
                    );"""
                )
                return True
        # If wallet exists, add funds to the wallet
        else:
            wallet = get_wallet_by_currency(username, currency)[0]
            wallet_id = wallet[0]
            current_wallet_balance = wallet[3]
            new_wallet_balance = current_wallet_balance + balance
            engine.execute(f"""
                UPDATE wallets
                SET balance = {new_wallet_balance}
                WHERE id = {wallet_id}
                ;"""
            )
            return True
    except Exception as e:
        print(f'Oops! there was an exception :(  {e}')
        return False

# Take funds out of a wallet
def subtract_wallet(username, balance, currency):
    engine = init()
    try:
        wallet = get_wallet_by_currency(username, currency)[0]
        wallet_id = wallet[0]
        current_wallet_balance = wallet[3]
        new_wallet_balance = current_wallet_balance - balance
        engine.execute(f"""
            UPDATE wallets
            SET balance = {new_wallet_balance}
            WHERE id = {wallet_id}
            ;"""
        )
        return True
    except Exception as e:
        print(f'Oops! there was an exception :(  {e}')
        return False
