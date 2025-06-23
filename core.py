# Нужно переделать на получение реальных данных с WB 

import sqlite3 as sq
import random
import requests

def create_db():
    with sq.connect('catalog.db') as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS items (
                        art INTEGER PRIMARY KEY,
                        name TEXT,
                        price TEXT,
                        description TEXT
        )''')

def insert_new_item(art, name, price, description):
    with sq.connect('catalog.db') as con:
        cur = con.cursor()
        cur.execute("INSERT OR IGNORE INTO items (art, name, price, description) VALUES (?, ?, ?, ?)",
                    (art, name, price, description))

def add_random_items(count=5):
    for _ in range(count):
        art = random.randint(100000000, 999999999)
        name = f"RandomItem{random.randint(1,1000)}"
        price = str(random.randint(1000, 20000))
        description = "" if random.choice([True, False]) else f"Description{random.randint(1,100)}"
        insert_new_item(art, name, price, description)

def create_indexes():
    with sq.connect('catalog.db') as con:
        cur = con.cursor()
        cur.execute("CREATE INDEX IF NOT EXISTS idx_items_art ON items (art)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_items_price ON items (price)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_items_description ON items (description)")

def show_all_items():
    print("\n[ ВСЕ ТОВАРЫ ]")
    with sq.connect('catalog.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM items")
        for row in cur.fetchall():
            print(row)

def items_without_description():
    print("\n[ ТОВАРЫ БЕЗ ОПИСАНИЯ ]")
    with sq.connect('catalog.db') as con:
        cur = con.cursor()
        cur.execute("SELECT art, name FROM items WHERE description IS NULL OR description = ''")
        for row in cur.fetchall():
            print(row)

def items_below_10000():
    print("\n[ ТОВАРЫ ДО 10.000 ]")
    with sq.connect('catalog.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM items WHERE CAST(price AS INTEGER) < 10000")
        for row in cur.fetchall():
            print(row)

def create_view_items_below_10000():
    with sq.connect('catalog.db') as con:
        cur = con.cursor()
        cur.execute("DROP VIEW IF EXISTS items_below_10000")
        cur.execute('''
            CREATE VIEW items_below_10000 AS
            SELECT * FROM items
            WHERE CAST(price AS INTEGER) < 10000
            ORDER BY CAST(price AS INTEGER) ASC
        ''')

def show_items_view():
    print("\n[ ПРЕДСТАВЛЕНИЕ: ДО 10.000 ]")
    with sq.connect('catalog.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM items_below_10000")
        for row in cur.fetchall():
            print(row)

# ---------- Запуск ----------
create_db()
insert_new_item(111111111, "ManualProduct", "8888", "Manual description")
add_random_items(10)
create_indexes()
show_all_items()
items_without_description()
items_below_10000()
create_view_items_below_10000()
show_items_view()
