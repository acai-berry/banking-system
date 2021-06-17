import sqlite3

CREATE_CARD_TABLE = """CREATE TABLE IF NOT EXISTS card (
                        id INTEGER PRIMARY KEY,
                        number TEXT,
                        pin TEXT,
                        balance INTEGER DEFAULT 0
                        );
                        """
INSERT_CARD = "INSERT INTO card (number, pin) VALUES (?,?)"

CHANGE_BALANCE = "UPDATE card SET balance = ? WHERE number = ?"


SHOW_BALANCE = "SELECT balance FROM card WHERE number=?"

SELECT_CARD = "SELECT number, pin FROM card WHERE number=?"

SELECT_CARD_PIN = "SELECT number, pin FROM card WHERE number=? AND pin = ?"

DELETE_ACCOUNT = 'DELETE FROM card WHERE number = ? '


def connect():
    return sqlite3.connect("card.s3db")

def create_table(connection):
    # cur.execute("DROP TABLE card")
    with connection:
        connection.execute(CREATE_CARD_TABLE)

def add_card(connection, number, pin):
    with connection:
        connection.execute(INSERT_CARD, (number, pin))

def select_card(connection, number):
    with connection:
        return connection.execute(SELECT_CARD, (number,)).fetchone()

def select_card_pin(connection, number, pin):
    with connection:
        return connection.execute(SELECT_CARD_PIN, (number, pin)).fetchone()


def change_balance(connection, amount, number):
    with connection:
        return connection.execute(CHANGE_BALANCE, (amount, number)).fetchone()

def show_balance(connection, number):
    with connection:
        return connection.execute(SHOW_BALANCE, (number,)).fetchone()

def delete_account(connection, number):
    with connection:
        return connection.execute(DELETE_ACCOUNT, (number,))

