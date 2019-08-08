import constants
import sqlite3
from sqlite3 import Error
from tkinter import messagebox


# ŁĄCZENIE Z BAZĄ DANYCH
def create_connection(db_file):
    try:
        conn= sqlite3.connect(db_file)
        return conn
    except Error as e:
        messagebox.showinfo(constants.DB_NAME, "Nie udało się połączyć z bazą danych: ", e)
        return None


# TWORZENIE GŁÓWNEJ BAZY DANYCH
def create_program_table(conn):
    try:
        create_table_sql = 'CREATE TABLE IF NOT EXISTS ' + constants.DB_TABLE_NAME + """(
                            id integer PRIMARY KEY NOT NULL,
                            name NVARCHAR UNIQUE NOT NULL,
                            type NVARCHAR NOT NULL,
                            description NVARCHAR,
                            notes NTEXT,
                            modification_time DATETIME);"""
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        messagebox.showerror(constants.DB_NAME, "Nie udało się utworzyć tabeli " + constants.DB_TABLE_NAME + ": " + str(e))


def add_item(conn, item):
    try:
        sql = 'INSERT INTO ' + constants.DB_TABLE_NAME + """(name, type, description, notes, modification_time) VALUES (?, ?, ?, ?, ?);"""
        c = conn.cursor()
        c.execute(sql, item)
        conn.commit()
        return c.lastrowid
    except Error as e:
        messagebox.showerror(constants.DB_NAME, "Nie udało się dodać obiektu do tabeli: " + str(e))
        return None


def delete_item(conn, item_name):
    try:
        sql = 'DELETE FROM ' + constants.DB_TABLE_NAME + ' WHERE name=?'
        c = conn.cursor()
        c.execute(sql, (item_name,))
        conn.commit()
    except Error as e:
        messagebox.showerror(constants.DB_NAME, "Błąd podczas usuwania " + item_name + ": " + str(e))


def get_notes(conn, item_name):
    c = conn.cursor()
    c.execute("SELECT notes FROM " + constants.DB_TABLE_NAME + " WHERE name = '" + item_name + "';")
    notes = c.fetchall()
    return notes


def get_description(conn, item_name):
    c = conn.cursor()
    c.execute("SELECT description FROM " + constants.DB_TABLE_NAME + " WHERE name = '" + item_name + "';")
    notes = c.fetchall()
    return notes


def get_type(conn, item_name):
    c = conn.cursor()
    c.execute("SELECT type FROM " + constants.DB_TABLE_NAME + " WHERE name = '" + item_name + "';")
    notes = c.fetchall()
    return notes


def select_all_items(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM " + constants.DB_TABLE_NAME)
    rows = c.fetchall()
    return rows


def select_all_users(conn):
    c = conn.cursor()
    c.execute("SELECT name, description, modification_time FROM " + constants.DB_TABLE_NAME + " WHERE type = '" + constants.DB_USER_TYPE_NAME + "' ORDER BY name;")
    rows = c.fetchall()
    return rows


def select_all_computers(conn):
    c = conn.cursor()
    c.execute("SELECT name, description, modification_time FROM " + constants.DB_TABLE_NAME + " WHERE type = '" + constants.DB_COMPUTER_TYPE_NAME + "' ORDER BY name;")
    rows = c.fetchall()
    return rows


def select_all_devices(conn):
    c = conn.cursor()
    c.execute("SELECT name, description, modification_time FROM " + constants.DB_TABLE_NAME + " WHERE type = '" + constants.DB_DEVICE_TYPE_NAME + "' ORDER BY name;")
    rows = c.fetchall()
    return rows


def select_all_programs(conn):
    c = conn.cursor()
    c.execute("SELECT name, description, modification_time FROM " + constants.DB_TABLE_NAME + " WHERE type = '" + constants.DB_PROGRAM_TYPE_NAME + "' ORDER BY name;")
    rows = c.fetchall()
    return rows


def select_all_tips(conn):
    c = conn.cursor()
    c.execute("SELECT name, description, modification_time FROM " + constants.DB_TABLE_NAME + " WHERE type = '" + constants.DB_TIP_TYPE_NAME + "' ORDER BY name;")
    rows = c.fetchall()
    return rows


def select_all_items_with_string(conn, string_value):
    c = conn.cursor()
    c.execute("SELECT type, name, description, modification_time FROM " + constants.DB_TABLE_NAME + " WHERE name LIKE '%" + string_value + "%' OR description LIKE '%" + string_value + "%';")
    rows = c.fetchall()
    return rows


def select_all_items_with_string_in_notes(conn, string_value):
    c = conn.cursor()
    c.execute("SELECT type, name, description, modification_time FROM " + constants.DB_TABLE_NAME + " WHERE notes LIKE '%" + string_value + "%';")
    rows = c.fetchall()
    return rows


def select_and_order_items(conn, type, by, order):
    c = conn.cursor()
    c.execute("SELECT name, description, modification_time FROM " + constants.DB_TABLE_NAME + " WHERE type = '" + type + "' ORDER BY " + by + " " + order + ";")
    rows = c.fetchall()
    return  rows


def update_notes(conn, item_name, text):
    c = conn.cursor()
    try:
        sql = "UPDATE " + constants.DB_TABLE_NAME + " SET notes = ? WHERE name = ?"
        c.execute(sql, (text, item_name))
        conn.commit()
    except Error as e:
        messagebox.showerror(constants.DB_NAME, "Błąd podczas zapisu: " + str(e))


def update_modification_time(conn, item_name, time):
    c = conn.cursor()
    try:
        sql = "UPDATE " + constants.DB_TABLE_NAME + " SET modification_time = ? WHERE name = ?"
        c.execute(sql, (time, item_name))
        conn.commit()
    except Error as e:
        messagebox.showerror(constants.DB_NAME, "Błąd podczas aktualizacji czasu modyfikacji: " + str(e))


def update_name(conn, item_name, name):
    c = conn.cursor()
    try:
        sql = "UPDATE " + constants.DB_TABLE_NAME + " SET name = ? WHERE name = ?"
        c.execute(sql, (name, item_name))
        conn.commit()
    except Error as e:
        messagebox.showerror(constants.DB_NAME, "Błąd podczas zmiany nazwy: " + str(e))


def update_description(conn, item_name, description):
    c = conn.cursor()
    try:
        sql = "UPDATE " + constants.DB_TABLE_NAME + " SET description = ? WHERE name = ?"
        c.execute(sql, (description, item_name))
        conn.commit()
    except Error as e:
        messagebox.showerror(constants.DB_NAME, "Błąd podczas zmiany opisu: " + str(e))


def update_type(conn, item_name, t):
    c = conn.cursor()
    try:
        sql = "UPDATE " + constants.DB_TABLE_NAME + " SET type = ? WHERE name = ?"
        c.execute(sql, (t, item_name))
        conn.commit()
    except Error as e:
        messagebox.showerror(constants.DB_NAME, "Błąd podczas zmiany typu: " + str(e))
