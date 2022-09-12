#!/usr/bin/python
import sqlite3

#CONNECTION TO DATABASE
def connect_to_database(dbname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    return conn, cur

#CREATE TABLE IF NOT EXISTS
def create_table(conn, cur, table_name, columns):
    cur.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, columns))
    conn.commit()
    #print("Table {} created".format(table_name))
    return

#CLOSE CONNECTION
def close_connection(conn):
    conn.close()
    #print("Connection closed")
    return

#INSERT DATA INTO TABLE
def insert_data(conn, cur, table_name, data):
    cur.execute("INSERT INTO {} VALUES ({})".format(table_name, data))
    conn.commit()
    #print("Data inserted")
    return

#SELECT DATA FROM TABLE
def select_data(conn, cur, query):
    cur.execute(query)
    data = cur.fetchall()
    conn.commit()
    #print("Data selected")
    return data

#UPDATE DATA IN TABLE
def update_data(conn, cur, query):
    cur.execute(query)
    conn.commit()
    #print("Data updated")
    return

#READ ALL TABLES
def read_all_tables(dbname):
    conn, cur = connect_to_database(dbname)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    conn.commit()
    #print("Tables read")
    return tables
