#!/usr/bin/python
import sqlite3

#CONNECTION TO DATABASE
def connect_to_database(dbname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    return conn, cur

#CREATE TABLE IF NOT EXISTS
def create_table(conn, cur,table_name,columns):
    cur.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table_name,columns))
    conn.commit()
    print("Table {} created".format(table_name))
    return

#CLOSE CONNECTION
def close_connection(conn):
    conn.close()
    print("Connection closed")
    return

#INSERT DATA INTO TABLE
def insert_data(conn, cur, table_name,data):
    cur.execute("INSERT INTO {} VALUES ({})".format(table_name,data))
    conn.commit()
    print("Data inserted")
    return
