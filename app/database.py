import os
import sqlite3 as sq
import logging

db = sq.connect('tg.db')

cur = db.cursor()


async def db_start():
    sql_query = f'''
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER)
    '''

    try:
        cur.execute(sql_query)
        db.commit()
        logging.info("Table 'users' created successfully.")
    except Exception as e:
        logging.error(f"Error creating table: {e}")


async def save_user(user_id, name, age):
    sql_query = f'''
        INSERT INTO users (id, name, age) VALUES (?, ?, ?)
    '''

    try:
        cur.execute(sql_query, (user_id, name, age))
        db.commit()
        print(f"User {name} saved successfully.")
    except Exception as e:
        print(f"Error saving user: {e}")


async def get_user_list():
    sql_query = f'''
        SELECT * FROM users
    '''

    try:
        cur.execute(sql_query)
        rows = cur.fetchall()
        users = [dict(id=row[0], name=row[1], age=row[2]) for row in rows]
        print(f"Users list successfully retrieved")
        return users
    except Exception as e:
        print(f"Error getting user_list: {e}")
