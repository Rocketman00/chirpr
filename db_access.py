import sqlite3

from flask import app, g


def get_all_chirps():
    conn = get_db()
    return conn.execute('''
        SELECT c.id, c.body, c.datetime, u.handle
        FROM chirp c, user u
        WHERE c.user_id = u.id
    ''').fetchall()


def delete_chirp(chirp_id):
    conn = get_db()
    conn.execute('DELETE FROM chirp WHERE id = :id', {'id': chirp_id})
    conn.commit()


def get_all_users():
    conn = get_db()
    return conn.execute('SELECT id, handle FROM user').fetchall()


def delete_user(user_id):
    conn = get_db()
    conn.execute('DELETE FROM user WHERE id = :id', {'id': user_id})
    conn.commit()


def add_user(handle):
    conn = get_db()
    big_id, = conn.execute('SELECT MAX(id) AS id FROM user')
    conn.execute('INSERT INTO user (id, handle, admin) values (:id, :handle, :admin)',
                 {'id': big_id[0] + 1, 'handle': handle, 'admin': 0})
    conn.commit()


def get_db():
    if not hasattr(g, 'chirpr.db'):
        g.conn = connect_db()
    return g.conn


def connect_db():
    conn = sqlite3.connect('data/chirpr.db')
    conn.row_factory = sqlite3.Row
    return conn
