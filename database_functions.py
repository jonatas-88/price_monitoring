#!/usr/bin/python
import sqlite3

#function to connect to the database
def connect_to_database(dbname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    return conn, cur

#create table if it doesn't exist
def create_table(conn, cur,table_name,columns):
    cur.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table_name,columns))
    conn.commit()
    print("Table {} created".format(table_name))
    return

#close connection
def close_connection(conn):
    conn.close()
    print("Connection closed")
    return

#insert data into table
def insert_data(conn, cur, table_name,data):
    cur.execute("INSERT INTO {} VALUES ({})".format(table_name,data))
    conn.commit()
    print("Data inserted")
    return